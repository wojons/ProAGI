# Use a suitable Python base image
# Using a specific version for stability
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Install Poetry
# See https://python-poetry.org/docs/#installation
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy the pyproject.toml and poetry.lock files
# This allows Poetry to install dependencies
COPY ./sandbox/pyproject.toml ./pyproject.toml
# COPY ./sandbox/poetry.lock ./poetry.lock # Uncomment if you want to use a lock file

# Install dependencies
# The --no-root flag prevents Poetry from trying to install the current project as a package
# since package-mode = false is set in pyproject.toml
RUN poetry install --no-root

# Copy the application code
COPY ./sandbox/src/ ./src/

# Expose the port the FastAPI application will run on
EXPOSE 8080

# Command to run the FastAPI application using Uvicorn
# Assumes the main FastAPI app instance is named 'app' in 'src/main.py'
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

# TODO: Add health check instruction (Issue #XX)
# TODO: Configure logging within the container (Issue #XX)
# TODO: Consider a non-root user for security (Issue #XX)
