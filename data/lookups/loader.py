import json
from pathlib import Path

BASE_PATH = Path(__file__).parent


def load_ufs():
    with open(BASE_PATH / "ufs.json", encoding="utf-8") as f:
        data = json.load(f)

    by_id = {}
    by_sigla = {}
    # by_name = {}

    for uf in data:
        by_id[str(uf["id"])] = uf
        by_sigla[uf["sigla"]] = uf
        # by_name[uf["nome"]] = uf
        

    return by_id , by_sigla 


def load_municipios():
    with open(BASE_PATH / "municipios.json", encoding="utf-8") as f:
        data = json.load(f)

    municipios_by_6digits = {}
    for m in data:
        codigo_7 = str(m["id"])          # ex: "3106207"
        if len(codigo_7) == 7:
            codigo_6 = codigo_7[:6]      # ex: "310620"
            municipios_by_6digits[codigo_6] = m
        else:
            # Caso raro: código não tem 7 dígitos → use como está
            municipios_by_6digits[codigo_7] = m

    return municipios_by_6digits
