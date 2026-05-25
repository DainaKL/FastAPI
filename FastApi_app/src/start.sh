#!/bin/sh
set -e
alembic upgrade head
python -c "import asyncio; from src.core.init_admin import init_admin; asyncio.run(init_admin())"
exec uvicorn main:app --host 0.0.0.0 --port 8000
