# Nexus CoCreate AI

## Project Overview
Nexus CoCreate AI is a flexible and user-friendly agentic AI platform designed to empower users to easily create, deploy, manage, and share AI-powered applications and agents. Built upon the principles and architecture of the Ultra High Level Programming (UHLP) framework, it leverages an LLM as a dynamic runtime, enabling applications to be defined using high-level descriptions and workflows. The platform supports self-hosting, offers easy setup, and allows users to leverage their own API keys for various AI services or use platform-provided defaults.

## Key Features (POC)
-   Core backend architecture based on UHLP principles.
-   State management using Git/YAML (Definition/Config) and Redis (Runtime).
-   Basic database integration (PostgreSQL) for application data and framework metadata.
-   Basic secure API key validation logic.
-   Basic structure for the internal Sandbox API endpoint (`/execute`).
-   Basic placeholder logic for JIT Compilation within the Optimization Oracle.
-   Basic frontend file structure served by the backend.
-   Basic testing suite setup with pytest.
-   Basic CI/CD pipeline using GitHub Actions.

## Setup

### Prerequisites
-   Docker and Docker Compose installed.
-   Poetry installed (for backend development dependencies).

### Getting Started
1.  Clone the repository:
    ```bash
    git clone https://github.com/wojons/ProAGI.git
    cd ProAGI
    ```
2.  **Important:** Update the placeholder passwords in `docker-compose.yml` for the PostgreSQL service.
3.  Build and start the Docker containers for the backend, Redis, and PostgreSQL:
    ```bash
    docker-compose up --build
    ```
    This will build the backend Docker image, set up the Redis and PostgreSQL services, and start all containers. The backend application will automatically create the necessary database tables on startup (for POC).

### Installing Backend Development Dependencies
If you plan to contribute to the backend code or run tests locally outside of Docker:
```bash
cd backend
poetry install --only main,dev
```

## Running the Application
Once the Docker containers are running (`docker-compose up`), the backend API should be accessible at `http://localhost:8000`.

The basic frontend Admin Panel should be accessible in your web browser at `http://localhost:8000`.

## Running Tests
To run the backend tests locally (after installing development dependencies):
```bash
cd backend
poetry run pytest tests/backend
```

## Documentation
-   **Nexus CoCreate AI System Specification (v1):** [docs/Nexus_CoCreate_AI_Specification/v1.md](docs/Nexus_CoCreate_AI_Specification/v1.md)
-   **Memory Bank:** [memory-bank/](memory-bank/)

## Usage Examples
(TODO: Add examples for registering applications, making requests, etc. - Issue #XX)

## Contribution Guidelines
(TODO: Add contribution process - Issue #XX)

## License Information
(TODO: Add license text, e.g., MIT License - Issue #XX)
