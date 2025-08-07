#!/bin/sh

alembic upgrade head
uvicorn --host 0.0.0.0 --port 8080 --reload src.main:app
