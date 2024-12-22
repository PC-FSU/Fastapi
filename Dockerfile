# The builder image, used to build the virtual environment
FROM python:3.12 as builder

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12.8-slim-bullseye as runtime

# Install required libraries for psycopg2
RUN apt-get update && apt-get install -y libpq5 libpq-dev && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . .

# Copy the entrypoint script and make it executable
COPY alembic_setup.sh /alembic_setup.sh
RUN chmod +x /alembic_setup.sh

# Set entrypoint to run Alembic migrations
ENTRYPOINT ["/alembic_setup.sh"]

# Set CMD to run Uvicorn, only after Alembic migrations are done
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]