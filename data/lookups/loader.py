import json
from pathlib import Path

BASE_PATH = Path(__file__).parent


def load_ufs():
    with open(BASE_PATH / "ufs.json", encoding="utf-8") as f:
        data = json.load(f)

    by_sigla = {}
    by_id = {}

    for uf in data:
        by_sigla[uf["sigla"]] = uf
        by_id[str(uf["id"])] = uf

    return by_sigla, by_id


def load_municipios():
    with open(BASE_PATH / "municipios.json", encoding="utf-8") as f:
        data = json.load(f)

    return {str(m["id"]): m for m in data}
