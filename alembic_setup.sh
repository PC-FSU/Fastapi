#!/bin/bash

# No need to activate virtual environment as it's already in PATH
echo "Using Python from: $(which python)"
echo "Using Uvicorn from: $(which uvicorn)"

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Execute the main command (uvicorn)
exec "$@"