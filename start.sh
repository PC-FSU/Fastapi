#!/bin/bash
set -e  # Exit on error

# Run Alembic migrations
alembic upgrade head

# Start Uvicorn server
uvicorn app.main:app --host 0.0.0.0 --port 8000