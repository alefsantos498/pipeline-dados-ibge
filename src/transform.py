"""Transformações de dados IBGE."""
from __future__ import annotations

from pathlib import Path
import json
import pandas as pd  # type: ignore


def json_to_dataframe(json_path: Path) -> pd.DataFrame:
    """Converte o arquivo JSON em um DataFrame pandas.

    A estrutura da resposta da API do IBGE pode variar entre tabelas. Esta função
    executa uma normalização genérica; adapte conforme necessário.
    """
    with open(json_path, encoding="utf-8") as fp:
        raw_json = json.load(fp)

    df = pd.json_normalize(raw_json)
    return df 