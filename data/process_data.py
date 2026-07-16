import re
from collections import defaultdict
from pathlib import Path

import pandas as pd
from sqlalchemy.exc import IntegrityError

from core.models import DengueCase
from data.transformers.age import parse_age
from infra.database import SessionLocal

"""

# When the API was used

BASE_URL = os.getenv("OPENDATASUS_BASE_URL")
PAGE_SIZE = int(os.getenv("API_PAGE_SIZE", 1000))

HEADERS = {
    "accept": "application/json"
}


def fetch_dengue_data(nu_ano: int, limit: int, offset: int) -> list[dict]:
    params = {
        "nu_ano": nu_ano,
        "limit": limit,
        "offset": offset
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    # response.raise_for_status()
    data = response.json()

    return data.get("parametros", [])

"""


def load_csv_in_chunks(path: str, chunksize: int = 50_000):
    return pd.read_csv(path, chunksize=chunksize, low_memory=False)


def normalize_data(records: list[dict]) -> pd.DataFrame:
    """
    Normalize raw OpenDataSUS dengue data.

    Returns a DataFrame ready for persistence and downstream consumption.
    """

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # Date conversion
    date_columns = ["dt_notific", "dt_sin_pri", "dt_invest"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

    # Compound age field
    if "nu_idade_n" in df.columns:
        df[["idade", "idade_unidade"]] = df["nu_idade_n"].apply(
            lambda x: pd.Series(parse_age(x))
        )

    # Safe Int64 conversion
    integer_columns = [
        "tp_not",
        "sem_not",
        "sem_pri",
        "nu_ano",
        "sg_uf_not",
        "id_municip",
        "id_regiona",
        "ano_nasc",
        "idade",
        "cs_gestant",
        "cs_raca",
        "cs_escol_n",
        "sg_uf",
        "id_mn_resi",
        "id_rg_resi",
        "id_pais",
        "id_unidade",
    ]

    for col in integer_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Final column selection
    final_columns = [
        "tp_not",
        "id_agravo",
        "dt_notific",
        "sem_not",
        "nu_ano",
        "sg_uf_not",
        "id_municip",
        "id_regiona",
        "id_unidade",
        "dt_sin_pri",
        "sem_pri",
        "ano_nasc",
        "idade",
        "idade_unidade",
        "cs_sexo",
        "cs_gestant",
        "cs_raca",
        "cs_escol_n",
        "sg_uf",
        "id_mn_resi",
        "id_rg_resi",
        "id_pais",
        "dt_invest",
    ]

    final_columns = [c for c in final_columns if c in df.columns]

    return df[final_columns]


def save_to_database(df: pd.DataFrame) -> int:
    if df.empty:
        return 0

    session = SessionLocal()
    try:
        # Convert DataFrame rows to a list of dictionaries
        records = df.to_dict(orient="records")

        # Create DengueCase objects
        cases = [DengueCase(**r) for r in records]

        # Insert all records in a single transaction
        session.add_all(cases)
        session.commit()
        return len(cases)
    except IntegrityError as e:
        session.rollback()
        print("❌ Integrity error while inserting data:")
        print(e.orig)  # Shows the real database error
        raise
    finally:
        session.close()


def run_pipeline(csv_path: str, max_per_group: int = 100):
    """
    Read the CSV file once, keeping at most `max_per_group` records
    per (sg_uf_not, nu_ano, month).
    """

    MAX_BIGINT = 9_223_372_036_854_775_807
    MIN_BIGINT = -9_223_372_036_854_775_807

    # Buffer by group: (state, year, month) -> list of records
    sampled_groups = defaultdict(list)
    total_read = 0

    print("Reading CSV and applying stratified sampling...")
    for chunk in load_csv_in_chunks(csv_path):
        chunk.columns = chunk.columns.str.lower()
        chunk = chunk.dropna(subset=["dt_notific", "sg_uf_not", "nu_ano"])

        # Extract month
        chunk["mes"] = pd.to_datetime(chunk["dt_notific"], errors="coerce").dt.month
        chunk = chunk.dropna(subset=["mes"])

        # Convert critical fields
        chunk["sg_uf_not"] = pd.to_numeric(chunk["sg_uf_not"], errors="coerce").astype(
            "Int64"
        )
        chunk["nu_ano"] = pd.to_numeric(chunk["nu_ano"], errors="coerce").astype(
            "Int64"
        )
        chunk["mes"] = chunk["mes"].astype("Int64")

        bigint_cols = {
            "tp_not",
            "sem_not",
            "sem_pri",
            "nu_ano",
            "sg_uf_not",
            "id_municip",
            "id_regiona",
            "ano_nasc",
            "idade",
            "cs_gestant",
            "cs_raca",
            "cs_escol_n",
            "sg_uf",
            "id_mn_resi",
            "id_rg_resi",
            "id_pais",
            "id_unidade",
        }

        for record in chunk.to_dict(orient="records"):
            # First: try to extract the group key
            try:
                uf = int(record["sg_uf_not"])
                ano = int(record["nu_ano"])
                mes = int(record["mes"])
                key = (uf, ano, mes)
            except (TypeError, ValueError, KeyError):
                continue

            # Second: validate that all bigint fields are within range
            skip_record = False
            for col in bigint_cols:
                val = record.get(col)
                if val is not None and pd.notna(val):
                    try:
                        # Convert directly to int to avoid precision loss with float
                        if isinstance(val, str):
                            if val.strip() == "":
                                continue
                            num_val = int(val)
                        elif pd.isna(val):
                            continue
                        else:
                            # Can be numpy.int64, pandas.Int64, etc.
                            num_val = int(val)

                        if not (MIN_BIGINT <= num_val <= MAX_BIGINT):
                            skip_record = True
                            break
                    except (ValueError, TypeError, OverflowError):
                        skip_record = True
                        break

            if skip_record:
                continue

            # Third: add only if the group limit has not been reached yet
            if len(sampled_groups[key]) < max_per_group:
                sampled_groups[key].append(record)

        total_read += len(chunk)
        print(f"  Records read: {total_read} | Active groups: {len(sampled_groups)}")

    # Concatenate all selected records
    all_selected = [rec for group in sampled_groups.values() for rec in group]
    print(f"\nTotal records after sampling: {len(all_selected)}")

    # Normalize and save
    df_final = normalize_data(all_selected)
    if df_final.empty:
        print("No valid records to save.")
        return

    inserted = save_to_database(df_final)
    print(f"TOTAL inserted into database: {inserted}")


def _get_dengue_csv_files(raw_dir: str = "data/raw") -> list[Path]:
    """
    Return DENGBR*.csv files sorted by year.

    Example:
        DENGBR24.csv -> DENGBR25.csv
    """
    path = Path(raw_dir)

    files = []
    pattern = re.compile(r"DENGBR(\d{2})\.csv$", re.IGNORECASE)

    for file in path.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                year = int(match.group(1))
                files.append((year, file))

    # Sort by year: 24, 25, 26...
    files.sort(key=lambda x: x[0])

    # Return only Path objects
    return [f[1] for f in files]


if __name__ == "__main__":
    # run_pipeline("data/raw/DENGBR25.csv")

    csv_files = _get_dengue_csv_files("data/raw")

    if not csv_files:
        print("No DENGBR*.csv files found in data/raw")
        exit(1)

    for csv_path in csv_files:
        print(f"\nProcessing file: {csv_path.name}")
        run_pipeline(str(csv_path))
