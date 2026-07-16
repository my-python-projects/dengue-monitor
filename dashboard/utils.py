import json
from pathlib import Path


def load_ufs_for_select():
    """
    Return a list of (display_name, state_id) tuples.

    Example:
        [("Minas Gerais (31)", 31), ("São Paulo (35)", 35), ...]
    """
    base_path = Path(__file__).parent.parent / "data" / "lookups"
    with open(base_path / "ufs.json", encoding="utf-8") as f:
        ufs = json.load(f)

    # Sort by name for consistent display
    ufs_sorted = sorted(ufs, key=lambda x: x["nome"])
    return [(f"{uf['nome']} ({uf['sigla']})", uf["id"]) for uf in ufs_sorted]
