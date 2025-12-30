import pandas as pd
from typing import Optional, Tuple


def parse_idade(value) -> Tuple[Optional[int], Optional[str]]:
    """
    Interpreta o campo nu_idade_n do SINAN (DATASUS).

    Formato: UAAA
        U = unidade de tempo
            1 = horas
            2 = dias
            3 = meses
            4 = anos
            9 = ignorado
        AAA = valor da idade

    Exemplos:
        3009 -> 9 meses
        4018 -> 18 anos
    """
    if pd.isna(value):
        return None, None

    try:
        value = int(value)
    except (ValueError, TypeError):
        return None, None

    unidade_code = value // 1000
    idade = value % 1000

    if unidade_code == 9:
        return None, None

    unidade_map = {
        1: "horas",
        2: "dias",
        3: "meses",
        4: "anos",
    }

    unidade = unidade_map.get(unidade_code)

    if unidade is None:
        return None, None

    # validações básicas
    if idade <= 0:
        return None, None

    return idade, unidade
