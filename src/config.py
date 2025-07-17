"""Configurações globais do pipeline."""
from __future__ import annotations

import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

# Lançará KeyError se qualquer variável estiver ausente, facilitando a detecção de configuração incorreta
GCP_PROJECT_ID: str = os.environ["GCP_PROJECT_ID"]
GCS_BUCKET_RAW: str = os.environ["GCS_BUCKET_RAW"]
GCS_BUCKET_PROCESSED: str = os.environ["GCS_BUCKET_PROCESSED"]
BQ_DATASET: str = os.environ["BQ_DATASET"]
BQ_TABLE: str = os.environ["BQ_TABLE"] 