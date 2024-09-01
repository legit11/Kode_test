#!/bin/bash

alembic upgrade head

exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4