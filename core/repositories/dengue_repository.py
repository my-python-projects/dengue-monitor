from sqlalchemy.orm import Session
from sqlalchemy import func
from core.models import DengueCase


def get_cases_by_uf_and_year(
    db: Session,
    uf: int,
    ano: int,
    mes: int | None = None
):  
    query = (
        db.query(
            DengueCase.nu_ano.label("ano"),
            DengueCase.sg_uf_not.label("uf"),
            DengueCase.id_municip.label("municipio"),
            func.count(DengueCase.id).label("casos")
        )
        .filter(
            DengueCase.sg_uf_not == uf,
            DengueCase.nu_ano == ano
        )
    )

    if mes is not None:
        query = query.filter(func.extract('month', DengueCase.dt_notific) == mes)

    return query.group_by(
        DengueCase.nu_ano,
        DengueCase.sg_uf_not,
        DengueCase.id_municip
    ).all()



def get_cases_by_month(db: Session, uf_code: int, ano: int):
    return (
        db.query(
            func.extract("month", DengueCase.dt_notific).label("mes"),
            func.count(DengueCase.id).label("casos")
        )
        .filter(
            DengueCase.sg_uf_not == uf_code,
            DengueCase.nu_ano == ano,
            DengueCase.dt_notific.isnot(None)
        )
        .group_by(func.extract("month", DengueCase.dt_notific))
        .order_by("mes")
        .all()
    )  


def get_cases_by_age_group(db: Session, uf_code: int | None = None, ano: int | None = None, mes: int | None = None):
    query = db.query(DengueCase.id, DengueCase.idade)

    # Filtros opcionais
    if uf_code is not None:
        query = query.filter(DengueCase.sg_uf_not == uf_code)
    if ano is not None:
        query = query.filter(DengueCase.nu_ano == ano)
    if mes is not None:
        query = query.filter(func.extract("month", DengueCase.dt_notific) == mes)

    # Excluir idades nulas ou inválidas
    query = query.filter(DengueCase.idade.isnot(None), DengueCase.idade >= 0)

    subq = query.subquery()

    # Agrupar por faixa etária
    age_group = (subq.c.idade // 10).label("grupo")
    return (
        db.query(
            age_group,
            func.count().label("casos")
        )
        .group_by(age_group)
        .order_by(age_group)
        .all()
    )