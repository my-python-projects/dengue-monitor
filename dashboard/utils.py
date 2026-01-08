import json
from pathlib import Path

def load_ufs_for_select():
    """
    Retorna lista de tuplas (nome_exibicao, id_uf)
    Ex: [("Minas Gerais (31)", 31), ("São Paulo (35)", 35), ...]
    """
    base_path = Path(__file__).parent.parent / "data" / "lookups"
    with open(base_path / "ufs.json", encoding="utf-8") as f:
        ufs = json.load(f)
    
    # Ordena por nome para exibição consistente
    ufs_sorted = sorted(ufs, key=lambda x: x["nome"])
    return [(f"{uf['nome']} ({uf['sigla']})", uf["id"]) for uf in ufs_sorted]