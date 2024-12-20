# --- Builder Stage ---
# Use a lightweight Python 3.12 image for installing dependencies
FROM python:3.12-bullseye as builder

# Install Poetry, a dependency management tool for Python
RUN pip install poetry==1.8.2

# Disable interactive prompts for Poetry
ENV POETRY_NO_INTERACTION=1 \
    # Create virtual environments within the project directory
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    # Ensure a virtual environment is created
    POETRY_VIRTUALENVS_CREATE=1 \
    # Set the Poetry cache directory
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the dependency files into the container
COPY pyproject.toml poetry.lock ./

# Copy README.md if it exists (to satisfy Poetry's dependency check)
COPY README.md ./

# Uncomment this is there's dev depedency section in pyproject.toml. In that case comment the line below this one.
# # Install dependencies using Poetry with caching to speed up builds
# RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

# Install dependencies using Poetry with caching to speed up builds -- no dev dependency
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root


# --- Runtime Stage ---
# Use a smaller, minimal Python 3.12 image for running the application
FROM python:3.12-slim-bullseye as runtime

# Set the virtual environment path and update the PATH variable
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Set the working directory for the runtime container
WORKDIR /app

# Copy the virtual environment created in the builder stage
# COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder /usr/src/app/.venv /app/.venv

# Copy the application code into the runtime container
COPY . .

# Expose the port that the application will run on (adjust if necessary)
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# Build and Run Commands

# Build the Docker Image:
# ```DOCKER_BUILDKIT=1 docker build -t my_project_image . ```

# Run the Container:
# ```docker run -p 8000:8000 my_project_image```

