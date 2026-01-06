from data.lookups.loader import load_ufs, load_municipios

ufs_by_id, ufs_by_sigla  = load_ufs()
# ufs_by_id, ufs_by_sigla, ufs_by_name  = load_ufs()
municipios = load_municipios()


def translate_uf(sigla: str) -> dict | None:
    """
    Retorna dados da UF a partir da sigla
    """
    uf = ufs_by_sigla.get(sigla.upper())
    return uf["id"] if uf else None


def translate_uf_by_code(codigo: str) -> dict | None:
    """
    Recebe código IBGE da UF e retorna o objeto completo
    """
    return ufs_by_id.get(str(codigo))


def translate_municipio(codigo: str) -> dict | None:
    """
    Recebe código IBGE do município
    """
    return municipios.get(str(codigo))
