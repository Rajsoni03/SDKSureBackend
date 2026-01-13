# Repository Guidelines

## Project Structure & Module Organization

The repository now contains a Django backend scaffold under `test_management_backend/`. Source lives under that folder with domain apps in `apps/`, configuration in `config/`, and supporting assets in `requirements/`, `docker/`, and `docs/`. Tests live under `test_management_backend/tests/`.

## Build, Test, and Development Commands

Development commands (from `test_management_backend/`):
- Install deps: `pip install -r requirements/development.txt`
- Run server: `python manage.py runserver`
- Run tests: `pytest`
- Docker dev stack: `docker compose up`

Production build references `docker/Dockerfile` and `docker-compose.prod.yml`; `requirements/production.txt` pins server deps. Collect static is handled in entrypoint during container start.

## Coding Style & Naming Conventions

Python formatting/linting defaults are configured via `pyproject.toml` (Black), `.isort.cfg` (isort), and `.flake8`. Keep modules in snake_case and follow Django/DRF conventions.

## Testing Guidelines

Testing uses pytest with pytest-django; config in `pytest.ini` targets `test_management_backend/tests` and matches `test_*.py` or `*_test.py` patterns. No coverage thresholds yet; see `requirements/testing.txt` for tooling.

## Commit & Pull Request Guidelines

Git history currently contains only the message "Initial commit," so no commit convention is established. Use short, imperative commit messages and keep each change focused. For pull requests, include a brief description of the change, note any testing performed, and link related issues if applicable. Add screenshots only when UI behavior is affected.
