from typing import Optional, Tuple

import pandas as pd


def parse_age(value) -> Tuple[Optional[int], Optional[str]]:
    """
    Parse the SINAN (DATASUS) nu_idade_n field.

    Format: UAAA
        U = time unit
            1 = hours
            2 = days
            3 = months
            4 = years
            9 = unknown
        AAA = age value

    Examples:
        3009 -> 9 months
        4018 -> 18 years
    """
    if pd.isna(value):
        return None, None

    try:
        value = int(value)
    except (ValueError, TypeError):
        return None, None

    unit_code = value // 1000
    age = value % 1000

    if unit_code == 9:
        return None, None

    unit_map = {
        1: "horas",
        2: "dias",
        3: "meses",
        4: "anos",
    }

    unit = unit_map.get(unit_code)

    if unit is None:
        return None, None

    # Basic validations
    if age <= 0:
        return None, None

    return age, unit
