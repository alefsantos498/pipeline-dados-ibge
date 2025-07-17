"""Módulo responsável pela coleta de dados do IBGE."""
from __future__ import annotations

from pathlib import Path
import time
import requests  # type: ignore


# configuração simples de backoff exponencial para erros temporários
_MAX_RETRIES = 3
_BACKOFF_SECONDS = 2


def download_ibge_json(url: str, destination: Path) -> Path:
    """Faz o download de um endpoint JSON do IBGE e salva localmente.

    Parameters
    ----------
    url : str
        URL da requisição.
    destination : Path
        Caminho de destino do arquivo JSON.

    Returns
    -------
    Path
        O caminho do arquivo salvo.
    """
    attempt = 0
    while True:
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()

            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(response.text, encoding="utf-8")
            return destination
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response else None
            if status and 500 <= status < 600 and attempt < _MAX_RETRIES:
                attempt += 1
                wait = _BACKOFF_SECONDS ** attempt
                print(f"[WARN] Erro {status} na API IBGE. Tentativa {attempt}/{_MAX_RETRIES} em {wait}s…")
                time.sleep(wait)
                continue
            raise 