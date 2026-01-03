from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from api.schemas import DengueCaseOut
from core.repositories.dengue_repository import get_cases_by_uf_and_year

from api.services.location_service import (
    translate_uf,
    translate_uf_by_code,
    translate_municipio
)

router = APIRouter(prefix="/dengue", tags=["Dengue"])

@router.get("/cases", response_model=list[DengueCaseOut])
def list_cases(
    uf: str = Query(..., min_length=2, max_length=2),
    ano: int = Query(..., ge=2000),
    db: Session = Depends(get_db),
):
    
    print(f"UF: {uf}  -  ano: {ano}")

    uf_code = translate_uf(uf)  

    if not uf_code:
        return []

    rows = get_cases_by_uf_and_year(db, uf_code, ano)

    print(rows)

    result = []

    for row in rows:
        uf_info = translate_uf_by_code(row.uf)  # código -> dados
        mun_info = translate_municipio(row.municipio)

        result.append({
            "ano": int(row.ano),
            "uf": row.uf,
            "uf_nome": uf_info["nome"] if uf_info else "Desconhecido",
            "municipio": {
                "codigo": row.municipio,
                "nome": mun_info["nome"] if mun_info else "Desconhecido"
            },
            "casos": row.casos
        })

    return result


'''
@router.get("/casos/total")
def total_casos():
    pass

@router.get("/casos/por-mes")
def casos_por_mes():
    pass

@router.get("/ranking/estados")
def ranking_estados():
    pass
'''
