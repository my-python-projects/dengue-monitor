import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

# Importa conexão e model
from api.database import SessionLocal
from api.models import DengueCase

load_dotenv()

BASE_URL = os.getenv("OPENDATASUS_BASE_URL")
PAGE_SIZE = int(os.getenv("API_PAGE_SIZE", 1000))

HEADERS = {
    "accept": "application/json"
}

def fetch_dengue_data(nu_ano: int, limit: int, offset: int):

    params = {
        "nu_ano": nu_ano,
        "limit": limit,
        "offset": offset
    }
    response = requests.get(
        BASE_URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    # response.raise_for_status()

    data = response.json()
    records = data.get("parametros", [])

    return records


if __name__ == "__main__":
    dados = fetch_dengue_data(2025, limit=5, offset=0)
    print(dados[0])


