import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.schemas import AgeGroupCasesOut, DengueCaseOut, GenderCasesOut, MonthlyCasesOut
from api.services.location_service import (
    translate_municipio,
    translate_uf,
    translate_uf_by_code,
)
from core.repositories.dengue_repository import (
    get_cases_by_age_group,
    get_cases_by_gender,
    get_cases_by_month,
    get_cases_by_uf_and_year,
)
from infra.database import get_db

router = APIRouter(prefix="/dengue", tags=["Dengue"])
logger = logging.getLogger(__name__)


@router.get("/cases", response_model=list[DengueCaseOut])
def list_cases(
    uf: str = Query(..., min_length=2, max_length=2),
    ano: int = Query(..., ge=2024),
    mes: int | None = Query(None, ge=1, le=12),  # opcional
    db: Session = Depends(get_db),
):

    logger.info(
        "Starting dengue cases query",
        extra={"uf": uf, "ano": ano, "mes": mes},
    )

    uf_code = _convert_uf_to_code(uf)

    try:
        rows = get_cases_by_uf_and_year(db, uf_code, ano, mes)

    except SQLAlchemyError as exc:
        logger.exception(
            "Error querying the database", extra={"uf": uf, "ano": ano, "mes": mes}
        )
        raise HTTPException(
            status_code=500,
            detail="Internal error while querying data",
        ) from exc

    result = __map_cases(uf, rows)

    return result


def _convert_uf_to_code(uf):
    uf_code = translate_uf(uf)

    if not uf_code:
        logger.warning("Invalid state code provided", extra={"uf": uf})
        raise HTTPException(status_code=400, detail="Invalid state code")

    return uf_code


def __map_cases(uf, rows):
    result = []

    for row in rows:
        uf_info = translate_uf_by_code(row.uf)
        mun_info = translate_municipio(row.municipio)

        result.append(
            {
                "ano": int(row.ano),
                "uf": {
                    "id": row.uf,
                    "sigla": uf,
                    "nome": uf_info["nome"] if uf_info else "Desconhecido",
                },
                "municipio": {
                    "codigo": row.municipio,
                    "nome": mun_info["nome"] if mun_info else "Desconhecido",
                },
                "casos": row.casos,
            }
        )

    logger.info("Query completed successfully", extra={"total_registros": len(result)})

    return result


@router.get("/cases/by-month", response_model=list[MonthlyCasesOut])
def list_cases_by_month(
    uf: str = Query(..., min_length=2, max_length=2),
    ano: int = Query(..., ge=2000, le=2030),
    db: Session = Depends(get_db),
):
    uf_code = translate_uf(uf)
    if uf_code is None:
        return []

    rows = get_cases_by_month(db, uf_code, ano)

    return [{"mes": row.mes, "casos": row.casos} for row in rows if row.mes is not None]


def format_age_group(grupo: int) -> str:
    if grupo >= 9:  # 90+
        return "90+"
    return f"{grupo * 10}-{grupo * 10 + 9}"


@router.get("/cases/by-age-group", response_model=list[AgeGroupCasesOut])
def list_cases_by_age_group(
    uf: str = Query(..., min_length=2, max_length=2),
    ano: int = Query(..., ge=2000, le=2030),
    mes: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
):

    logger.info("Querying cases by age group", extra={"uf": uf, "ano": ano, "mes": mes})

    uf_code = _convert_uf_to_code(uf)

    try:
        rows = get_cases_by_age_group(db, uf_code, ano, mes)

    except SQLAlchemyError as exc:
        logger.exception(
            "Error querying the database", extra={"uf": uf, "ano": ano, "mes": mes}
        )
        raise HTTPException(
            status_code=500,
            detail="Internal error while querying data",
        ) from exc

    result = _map_age_group(rows)

    logger.info("Query completed", extra={"total_registros": len(result)})

    return result


def _map_age_group(rows):
    return [
        {
            "faixa_etaria": format_age_group(row.grupo),
            "casos": row.casos,
        }
        for row in rows
    ]


@router.get("/cases/by-gender", response_model=GenderCasesOut)
def list_cases_by_gender(
    uf: str | None = Query(None, min_length=2, max_length=2),
    ano: int | None = Query(None, ge=2000, le=2030),
    mes: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db),
):
    uf_code = None
    if uf:
        uf_code = translate_uf(uf)
        if uf_code is None:
            # Invalid state code → return zeros
            return {"masculino": 0, "feminino": 0, "ignorado": 0}

    row = get_cases_by_gender(db, uf_code, ano, mes)

    return {
        "masculino": int(row.masculino or 0),
        "feminino": int(row.feminino or 0),
        "ignorado": int(row.ignorado or 0),
    }
