from data.lookups.loader import load_municipios, load_ufs

ufs_by_id, ufs_by_sigla = load_ufs()
# ufs_by_id, ufs_by_sigla, ufs_by_name  = load_ufs()
municipios = load_municipios()


def translate_uf(sigla: str) -> dict | None:
    """
    Returns state data given its two-letter abbreviation
    """
    uf = ufs_by_sigla.get(sigla.upper())
    return uf["id"] if uf else None


def translate_uf_by_code(codigo: str) -> dict | None:
    """
    Takes a state's IBGE code and returns the complete state object.
    """
    return ufs_by_id.get(str(codigo))


def translate_municipio(codigo: str) -> dict | None:
    """
    Takes a municipality/city IBGE code.
    """
    return municipios.get(str(codigo))
