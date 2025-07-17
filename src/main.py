"""Script principal do pipeline IBGE."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from . import config
from .extract import download_ibge_json
from .transform import json_to_dataframe
from .load import upload_to_gcs, load_dataframe_to_bigquery

# Usamos apenas o último período para evitar resposta muito grande do servidor IBGE
IBGE_API_URL = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/7060"
    "/periodos/2025/variaveis/107?localidades=N1"
)


def run() -> None:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    raw_file = Path("data") / "raw" / f"{today}_ibge_raw.json"
    processed_file = Path("data") / "processed" / f"{today}_ibge.parquet"

    # EXTRAÇÃO
    download_ibge_json(IBGE_API_URL, raw_file)

    # TRANSFORMAÇÃO
    df = json_to_dataframe(raw_file)
    processed_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(processed_file, index=False)

    # CARGA PARA GCS
    upload_to_gcs(raw_file, config.GCS_BUCKET_RAW, f"ibge/raw/{raw_file.name}")
    upload_to_gcs(processed_file, config.GCS_BUCKET_PROCESSED, f"ibge/processed/{processed_file.name}")

    # CARGA PARA BIGQUERY
    load_dataframe_to_bigquery(df, config.BQ_DATASET, config.BQ_TABLE, project_id=config.GCP_PROJECT_ID)


if __name__ == "__main__":
    run() 