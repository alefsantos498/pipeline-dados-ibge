# Pipeline de Dados IBGE → GCP → BigQuery

Este projeto implementa um pipeline em Python para coletar, transformar e carregar dados de indicadores sociais e demográficos fornecidos pelo IBGE. Os dados brutos e os dados tratados são armazenados no Google Cloud Storage, e posteriormente carregados para o BigQuery para possibilitar análises e consultas avançadas.

## Etapas

1. **Extração**  
   - Coleta de dados via API do IBGE ou web scraping.

2. **Transformação**  
   - Conversão dos dados brutos em `pandas.DataFrame` e limpeza básica.

3. **Carga**  
   - Upload dos arquivos para buckets do Cloud Storage (camadas `raw` e `processed`).  
   - Carga dos dados tratados na tabela do BigQuery.

## Estrutura do Projeto

```
PIPELINE DE DADOS IBGE/
├── data/
│   ├── raw/          # Armazena arquivos brutos locais (facilita debug)
│   └── processed/    # Armazena arquivos transformados locais
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── config.py
│   └── main.py
├── requirements.txt
└── .env.example
```

## Pré-requisitos

- Python 3.10+
- Conta no GCP com projeto habilitado
- Service Account com permissões de Storage Admin e BigQuery Data Editor
- Variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` apontando para o JSON da service account

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuração

1. Copie o arquivo `env.example` para `.env` e ajuste as variáveis conforme seu ambiente.  
2. Certifique-se de que a variável `GOOGLE_APPLICATION_CREDENTIALS` esteja exportada ou definida no `.env`.

## Execução

```bash
python -m src.main
```

Isso irá:

- Buscar os dados do IBGE
- Gerar arquivos locais em `data/`
- Enviar arquivos para os buckets configurados
- Popular/atualizar a tabela no BigQuery

## Próximos Passos

- Implementar rotinas de agendamento (ex.: Cloud Functions, Cloud Composer/Airflow).
- Criar testes unitários.
- Adicionar mais indicadores do IBGE conforme necessidade. 

## Solução de Problemas (FAQ / Erros Comuns)

| Erro / Sintoma | Possível Causa | Como Resolver |
| -------------- | -------------- | ------------- |
| `KeyError: 'GCP_PROJECT_ID'` | Arquivo `.env` ausente ou variável vazia | Verifique se `.env` está na raiz do projeto e contém todas as variáveis necessárias. |
| `ModuleNotFoundError: No module named 'google'` | Dependências do Google Cloud não instaladas | Execute `pip install -r requirements.txt` ou `pip install google-cloud-storage google-cloud-bigquery`. |
| `ModuleNotFoundError: No module named 'requests'` | Dependências não instaladas | Rode `pip install -r requirements.txt`. |
| `pyarrow.lib.ArrowInvalid` ou erro ao salvar Parquet | Pacote `pyarrow` ausente | Certifique‐se de instalar as dependências (`pip install -r requirements.txt`). |
| `HTTPError: 5xx` ao chamar API do IBGE | Instabilidade no serviço do IBGE ou resposta muito grande | Tente novamente após alguns minutos ou reduza o período/escopo da consulta (ex.: peça um ano específico). |
| `google.api_core.exceptions.Forbidden` ao enviar para GCS/BigQuery | Service Account sem permissões adequadas | Garanta que a SA tenha papéis *Storage Admin* e *BigQuery Data Editor*. |
| `OSError: [Errno 13] Permission denied` no Windows ao acessar credenciais | Caminho da chave JSON incorreto ou protegido | Mova o arquivo `.json` para pasta sem restrições e atualize `GOOGLE_APPLICATION_CREDENTIALS` no `.env`. |

Caso encontre outro problema não documentado, abra uma *issue* ou entre em contato. 