from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from api.schemas import DengueCaseOut, MonthlyCasesOut, AgeGroupCasesOut

from core.repositories.dengue_repository import ( 
    get_cases_by_uf_and_year, 
    get_cases_by_month,
    get_cases_by_age_group
)

from api.services.location_service import (
    translate_uf,
    translate_uf_by_code,
    translate_municipio
)

router = APIRouter(prefix="/dengue", tags=["Dengue"])

@router.get("/cases", response_model=list[DengueCaseOut])
def list_cases(
    uf: str = Query(..., min_length=2, max_length=2),
    ano: int = Query(..., ge=2025),
    mes: int | None = Query(None, ge=1, le=12),  # opcional
    db: Session = Depends(get_db),
):

    uf_code = translate_uf(uf)  

    if not uf_code:
        return []

    rows = get_cases_by_uf_and_year(db, uf_code, ano, mes)

    result = []

    for row in rows:
        uf_info = translate_uf_by_code(row.uf)
        mun_info = translate_municipio(row.municipio)

        result.append({
            "ano": int(row.ano),
            "uf": {
                "id": row.uf,
                "sigla": uf,
                "nome": uf_info["nome"] if uf_info else "Desconhecido"
            },
            "municipio": {
                "codigo": row.municipio,
                "nome": mun_info["nome"] if mun_info else "Desconhecido"
            },
            "casos": row.casos
        })

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

    return [
        {"mes": row.mes, "casos": row.casos}
        for row in rows
        if row.mes is not None
    ]


def format_age_group(grupo: int) -> str:
    if grupo >= 9:  # 90+
        return "90+"
    return f"{grupo * 10}-{grupo * 10 + 9}"


@router.get("/cases/by-age-group", response_model=list[AgeGroupCasesOut])
def list_cases_by_age_group(
    uf: str | None = Query(None, min_length=2, max_length=2),
    ano: int | None = Query(None, ge=2000, le=2030),
    mes: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db),
):
    uf_code = translate_uf(uf) if uf else None
    if uf and uf_code is None:
        return []

    rows = get_cases_by_age_group(db, uf_code, ano, mes)

    return [
        {
            "faixa_etaria": format_age_group(row.grupo),
            "casos": row.casos,
        }
        for row in rows
    ]
