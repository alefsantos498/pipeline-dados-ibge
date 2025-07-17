"""Rotinas de carga para GCS e BigQuery."""
from __future__ import annotations

from pathlib import Path

import pandas as pd  # type: ignore
from google.cloud import storage, bigquery  # type: ignore
from google.cloud.exceptions import NotFound  # type: ignore


def upload_to_gcs(local_path: Path, bucket_name: str, destination_blob: str) -> None:
    """Envia um arquivo local para um bucket do Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(local_path)
    print(f"Arquivo {local_path} enviado para gs://{bucket_name}/{destination_blob}")


def load_dataframe_to_bigquery(
    df: pd.DataFrame,
    dataset_id: str,
    table_id: str,
    project_id: str | None = None,
    write_disposition: str = "WRITE_TRUNCATE",
) -> None:
    """Carrega um DataFrame para BigQuery."""
    client = bigquery.Client(project=project_id)

    # Cria dataset caso não exista
    try:
        client.get_dataset(dataset_id)
    except NotFound:
        dataset_ref = client.dataset(dataset_id)
        dataset = bigquery.Dataset(dataset_ref)
        client.create_dataset(dataset)
        print(f"Dataset {dataset_id} criado.")

    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)
    load_job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    load_job.result()
    print(f"Inseridos {load_job.output_rows} registros em {dataset_id}.{table_id}") 