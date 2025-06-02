# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-06-01

### Added
- Initial backend core structure with placeholder components.
- Basic FastAPI API endpoints for Applications, Requests, Tools, and Status.
- gRPC service definitions and generated Python stubs.
- Basic infrastructure setup using Docker Compose (Redis, PostgreSQL).
- Basic database integration with SQLModel and PostgreSQL.
- Basic secure API key validation logic (placeholder).
- Basic structure and Dockerfile for the internal Sandbox API endpoint.
- Basic placeholder logic for JIT Compilation within the Optimization Oracle.
- Basic frontend file structure and backend configuration to serve static files.
- Basic testing suite setup with pytest and a placeholder test file.
- Basic CI/CD pipeline using GitHub Actions.

### Changed
- Updated project goal and overview to reflect Nexus CoCreate AI platform focus.
- Refined initial implementations of core backend components with docstrings and TODOs.
- Updated `pyproject.toml` with necessary dependencies (FastAPI, Uvicorn, bcrypt, SQLAlchemy, SQLModel, psycopg2-binary, pytest, httpx).
- Updated `backend/src/main.py` to instantiate core components and run the FastAPI app.
- Updated `backend/src/core/application_registry/application_registry.py` with basic database and bcrypt integration for API key validation.
- Updated `README.md` with project overview, features, setup, running, and testing instructions.

### Removed
- Duplicate Core Framework API specification file.

### Fixed
- Resolved `python: command not found` error during gRPC stub generation.
- Resolved Poetry installation error related to missing README.md by setting `package-mode = false`.
- Resolved Poetry installation errors related to outdated lock file by running `poetry lock`.
