# Django Backend Setup (Draft)

## Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

## Local Development
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
pip install -r requirements/development.txt
python manage.py migrate
python manage.py runserver
```

## Docker (dev)
```bash
docker compose up --build
```

