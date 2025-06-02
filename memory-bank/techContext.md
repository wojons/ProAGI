# Tech Context

## Technologies (Core Nexus CoCreate AI Stack)

### Core Framework
- **Backend Core Language:** Python 3.10+ (as per UHLP standards) (Section 07.0).
- **Containerization:** Docker (for Sandboxed Components) (Section 06.1, 07.0).
- **State Management (Definition/Config):** Git + YAML files (Section 03.3.1).
- **State Management (Runtime):** Redis (Section 03.3.2).
- **Internal APIs:** gRPC (preferred for inter-component communication) and HTTP (Section 02.1, 03.5, 03.6, 03.17, 03.19).
- **Tool Integration Protocol:** MCP (Model Context Protocol) for standardized interactions (Section 03.8).
- **Configuration:** Environment variables primarily (Section 06.3).
- **Metrics:** OTLP-inspired push API, Prometheus exposition format (Section 02.1.7).
- **Optimization:** JIT compilation orchestrated by OptimizationOracle (Section 02.1.6).
- **Event Bus:** In-memory event bus for asynchronous communication.

### Dockerfile Best Practices & Base Images
- Multi-stage builds are optional; Nexus (LLM) will decide if it's the right choice for a specific project. This is not a core system enforcement.
- The system will provide a collection of slim/base Docker images as a starting point. These can be built upon to create more comprehensive Dockerfiles tailored to application needs.
- The system should guide users in selecting base images: A predefined list of curated slim/base images will be provided by the system. The LLM can then use these as a foundation or decide to build more complex images.
- Dockerfile linting (e.g., with hadolint) is not a core MVP requirement but could be a future enhancement.

### Sandboxed Components
- **Execution Environments:** Docker containers (JIT Runners, LLM Orchestrators) (Section 03.2, 06.1).
- **Internal API:** HTTP POST /execute endpoint (Section 03.5).
- **Languages:** Python (for JIT runners), potentially others (Section 02.1.5).
- **Templating:** Jinja2 (for Prompt Templates) (Section 03.18.1).
- **Workflow Execution:** Custom Python logic for interpreting YAML workflows.

### MCP Servers
- **Core Language:** Python (for CoreMCPServer), flexible for Community/App-Specific (Section 03.8).
- **Transport:** HTTP/1.1 (V1 target) (Section 03.8.5).
- **API Definition:** JSON Schema for tool inputs/outputs (Section 04.12).

### Frontend (Admin Panel / User UI)
- **Generation:** LLM-generated HTML/CSS/JS (V0.1 approach) (Section 03.20.4).
- **Serving:** Directly by the Core Framework (Section 03.20.4).
- **Interaction:** Calls to Core Framework internal APIs (HTTP/gRPC) (Section 03.20.5).
- **Styling/Interactivity:** Minimalist CSS/JS frameworks to guide LLM generation.

### Application Domain Data
- **Storage:** External Databases (SQL, NoSQL) or object storage (Section 03.3.3).
- **Access:** Exclusively via Community MCP Servers (Section 03.3.3).

## Development Setup
- **Containerization:** Docker, Docker Compose (essential for self-hosting and consistent environments) (Section 07.0).
- **IDE:** VSCode with relevant extensions.
- **Python Dependency Management:** Poetry (already in use).
- **Code Formatting/Linting:** Black, Flake8, Ruff for Python.
- **Testing Frameworks:** pytest.

## Deployment
- **Self-Hosting:** Docker Compose (primary method) (Section 07.0).
- **Cloud-Hosting (Future):** Considerations for Kubernetes, PaaS, Serverless (Section 07.3).

## Technical Constraints (Aligned with UHLP)
- **Performance:** Efficient execution within sandboxes, optimized via JIT (Section 02.1.6).
- **Scalability:** Design for horizontal scaling of Core Framework components and Sandbox pools (Section 07.3).
- **Security:** Adherence to UHLP security guidelines (sandboxing limitations, secured command execution, API key management, input validation, MCP scoping) (Section 06.0).
- **Compatibility:** Ensure self-hosting solution is broadly compatible via Docker (Section 07.0).
- **Extensibility:** Easy to add new MCP tools and potentially new sandbox types (Section 01.5).

## Dependencies (Core Nexus CoCreate AI POC)
- **Python:** 3.10+
- **Core Python Libs:**
    - FastAPI, Uvicorn (Core Framework HTTP/APIs)
    - grpcio, grpcio-tools (Internal gRPC communication)
    - docker-py (Sandbox Management)
    - GitPython (Definition/Config State - Git)
    - PyYAML (Definition/Config State - YAML parsing)
    - redis-py (Runtime State - Redis)
    - evently (Event Bus)
    - prometheus_client (Metrics Exposition)
    - SQLAlchemy, SQLModel (Framework DB interaction)
    - Pydantic (Data validation)
    - httpx (HTTP client)
    - cryptography (Potential for API key encryption)
    - Jinja2 (Prompt Templating)
- **Frontend Libs (for LLM generation guidance):**
    - Minimalist CSS Framework (e.g., Milligram, Pure.css)
    - Lightweight JS Library (e.g., Alpine.js)
- **External Services:**
    - Docker & Docker Compose
    - Git
    - Redis
    - PostgreSQL

## Tool Usage Patterns (via MCP)
- **State Access:** Reading/writing application state (core.state.*) (Section 03.15).
- **Configuration Access:** Retrieving application configuration (core.framework.getConfigValue) (Section 02.1.4).
- **Logging:** Sending structured logs (core.framework.logFrameworkMessage) (Section 03.10, 04.6).
- **LLM Invocation:** Generating text completions (core.llm.generate) (Section 02.1.5).
- **Command Execution:** Securely running Linux commands (core.linux.executeCommand) (Section 06.2).
- **Filesystem Access:** Reading/writing files on shared volumes (core.filesystem.* - Optional V1) (Section 03.7).
- **External Service Interaction:** Interacting with databases, APIs, etc. (community.*, app.*) (Section 03.8).
