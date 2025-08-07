# API example
Repo consisting of example API code for FastAPI-DB integration

# Prerequisites
## Dependencies:
- python 3.13.3
- poetry 2.1.4
- docker 28.1.1
- docker compose 2.33.1

## Setup development
1. Set your local python version, preferrably via `pyenv` or similar tool like `pipx` or `uv` to `3.13.3`
2. Set virtualenvs for poetry inside project: `poetry config virtualenvs.in-project true`
3. Activate virtualenv with command. For bash: `eval $(poetry env activate)`
4. Run `fastapi run src/main.py`
