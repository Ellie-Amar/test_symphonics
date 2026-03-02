# Test technique API

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Run with Docker
```bash
docker compose up --build
```

## Run locally (without Docker)
```bash
uvicorn app.main:app --reload
```

## Run tests
```bash
pytest
```

## Lint
```bash
ruff check .
black .
```
