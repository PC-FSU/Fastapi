#!/bin/bash

# Run Alembic migrations
echo "Running Alembic migrations..."
python -m alembic upgrade head

# After migrations, exit
exec "$@"
