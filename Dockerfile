FROM python:3.12

WORKDIR /usr/src/app

RUN pip install poetry

COPY . .

# Set the correct Python interpreter for Poetry.
RUN poetry env use python3.12

# Clear any previous virtual environment and install dependencies
RUN poetry env remove --all --yes || true
RUN poetry install --no-root


# Add virtual environment to PATH
ENV PATH="/usr/src/app/.venv/bin:$PATH"

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

