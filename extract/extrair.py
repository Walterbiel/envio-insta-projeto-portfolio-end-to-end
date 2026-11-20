"""Busca séries do Banco Central e grava em raw.indicadores (PostgreSQL)."""
import logging
from datetime import date, datetime

import psycopg2
import requests

SERIES = {"ipca": 433, "selic": 4390}
URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
INICIO = date(2020, 1, 1)

BANCO = dict(host="localhost", port=5432, dbname="indicadores", user="estudo", password="estudo")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("extract")


def buscar(codigo):
    params = {
        "formato": "json",
        "dataInicial": INICIO.strftime("%d/%m/%Y"),
        "dataFinal": date.today().strftime("%d/%m/%Y"),
    }
    resposta = requests.get(URL.format(codigo=codigo), params=params, timeout=30)
    resposta.raise_for_status()
    return resposta.json()          # [{"data": "01/01/2020", "valor": "0.21"}, ...]


def gravar(conexao, serie, registros):
    agora = datetime.now()
    with conexao.cursor() as cur:
        # Idempotente → apaga a série e grava de novo. Rodar 2 vezes dá o mesmo resultado
        cur.execute("DELETE FROM raw.indicadores WHERE serie = %s", (serie,))
        cur.executemany(
            "INSERT INTO raw.indicadores (serie, data, valor, extraido_em) VALUES (%s, %s, %s, %s)",
            [(serie, r["data"], r["valor"], agora) for r in registros],
        )


if __name__ == "__main__":
    with psycopg2.connect(**BANCO) as conexao:
        with conexao.cursor() as cur:
            cur.execute("CREATE SCHEMA IF NOT EXISTS raw")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS raw.indicadores (
                    serie TEXT, data TEXT, valor TEXT, extraido_em TIMESTAMP
                )
            """)
        for serie, codigo in SERIES.items():
            registros = buscar(codigo)
            gravar(conexao, serie, registros)
            log.info("%s → %s registros gravados em raw.indicadores", serie, len(registros))
