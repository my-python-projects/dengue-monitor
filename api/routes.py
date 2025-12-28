from fastapi import APIRouter

router = APIRouter()

@router.get("/casos")
def listar_casos(estado: str | None = None, ano: int | None = None):
    pass

@router.get("/casos/total")
def total_casos():
    pass

@router.get("/casos/por-mes")
def casos_por_mes():
    pass

@router.get("/ranking/estados")
def ranking_estados():
    pass
