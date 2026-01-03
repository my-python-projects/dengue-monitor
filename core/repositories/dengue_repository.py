from sqlalchemy.orm import Session
from sqlalchemy import func
from core.models import DengueCase


def get_cases_by_uf_and_year(
    db: Session,
    uf: str,
    ano: int
):
    return (
        db.query(
            DengueCase.nu_ano.label("ano"),
            DengueCase.sg_uf_not.label("uf"),
            DengueCase.id_municip.label("municipio"),
            func.count(DengueCase.id).label("casos")
        )
        .filter(
            DengueCase.sg_uf_not == uf,
            DengueCase.nu_ano == str(ano)
        )
        .group_by(
            DengueCase.nu_ano,
            DengueCase.sg_uf_not,
            DengueCase.id_municip
        )
        .all()
    )
