**Phase 1: Project Foundation & Core Interface Definitions**

- **Goal:** Set up the basic project structure, documentation, core standards, and define the essential interfaces and data structures that other components will rely on.
- **Tasks for Cline:**
    1. **Initialize Project Structure:** Create the main directories (`/core`, `/docs`, `/app_state_repo_template`, `/mcp_servers`, `/sandbox_images`, etc.) and basic configuration files (e.g., initial Python `requirements.txt` or `pyproject.toml` 01-core-framework.md, `.gitignore`).
    2. **Define Core Documentation:** Create `README.md` [1, 13] and `CHANGELOG.md` [1, 13], populating them with initial content based on `10-documentation.md`. Draft the ADR template [1, 13] in `/docs/adr`.
    3. **Establish Initial `.clinerules`:** Define rules based on the project standards documents, e.g., Python version 01-core-framework.md, mandatory async usage 01-core-framework.md, basic logging format 04-mcp-design.md, documentation update reminders [1, 13].
    4. **Define Core Data Structures:** Generate Python dataclasses or Pydantic models (or Protocol Buffer definitions if using gRPC extensively) for key structures like `AppDefinition`, `SandboxPoolConfig`, `ComponentDefinition`, `SecurityConfig` as described in Section 3.1.5 04 - State Management Details.md, Section 4 05 - Model Context Protocol (MCP).md, and throughout.
    5. **Define `StateManagerInterface` API:** Create the interface definition (e.g., Python abstract base class, or gRPC `.proto` file) specifying methods like `GetDefinitionFileContent`, `ApplyDefinitionDiff`, `SetRuntimeValue`, etc., based on Section 3.3 04 - State Management Details.md and Section 4.3 05 - Model Context Protocol (MCP).md.
    6. **Define `ApplicationRegistry` API:** Create the interface definition (e.g., ABC or gRPC `.proto`) for managing applications, specifying methods like `RegisterApplication`, `GetAppDetails`, `ListActiveApplications`, etc., based on Section 3.1 04 - State Management Details.md.
    7. **Define Core MCP Tool Schemas:** Create JSON Schema definitions for the input `params` and output `data` of the core MCP tools listed in Appendix B README.md and described in Section 5.2 04-mcp-design.md. Store these in a structured way (e.g., `/mcp_servers/core/schemas/`).
    8. **Define Sandbox `/execute` API Specification:** Create formal JSON Schema definitions for the `POST /execute` request body (`requestData`, `context`) and response body (`resultType`, `data`, `metrics`) based on Section 2.4 01 - Concept Overview.md and `02-sandbox-api.md` 02-sandbox-api.md.

**Phase 2: Core Framework Implementation (Initial)**

- **Goal:** Implement the essential backend services of the Core Framework.
- **Tasks for Cline:**
    1. **Implement `StateManagerInterface`:** Create the concrete implementation (using Python libraries for Git and Redis, based on Section 4 [6, 19]) adhering to the API defined in Phase 1. Include basic unit tests 09-testing.md.
    2. **Implement `ApplicationRegistry`:** Create the implementation (e.g., in-memory storage for V0.1, perhaps backed by the `StateManagerInterface` for persistence) adhering to the API defined in Phase 1. Include basic unit tests 09-testing.md.
    3. **Implement `CoreMCPServer`:** Create an HTTP server (e.g., using `aiohttp` 01-core-framework.md) that handles MCP requests [7, 20]. Implement routing logic and the actual functionality for core tools (like `core.state.*` calling the `StateManagerInterface`, `core.framework.*` calling `ApplicationRegistry`). Implement basic security checks [11, 25]. Requires unit and integration tests 09-testing.md.
    4. **Implement `SandboxManager`:** Implement the logic to interact with Docker (via docker-py library) to manage sandbox container lifecycles (create, start, stop, remove pools/instances) based on Section 3.2 04 - State Management Details.md. Implement the allocation API (`AllocateSandbox`/`ReleaseSandbox`). Requires unit tests (using mocking 09-testing.md) and integration tests 09-testing.md.
    5. **Implement `RequestRouter`:** Implement the core request handling flow: receive external request, use `ApplicationRegistry` to find the target component/app details, use `SandboxManager` to get a sandbox instance, call the sandbox's `/execute` endpoint, handle the response/errors (based on Section 2.3 01 - Concept Overview.md and component definitions 04 - State Management Details.md). Requires unit and integration tests 09-testing.md.

**Phase 3: Basic Sandbox Implementation**

- **Goal:** Create a minimal functional sandbox container that can receive requests from the Core Framework and interact via MCP.
- **Tasks for Cline:**
    1. **Create Base Sandbox Dockerfile:** Define a Dockerfile for a basic sandbox environment (e.g., Python base image, install necessary libraries, copy entry point script).
    2. **Implement Sandbox `/execute` Server:** Create the HTTP server inside the sandbox (e.g., basic Flask/FastAPI/Node Express) that listens on `POST /execute`, parses the request according to the spec from Phase 1, formats the response [5, 15], and handles basic transport errors. Adhere to `02-sandbox-api.md` standards 02-sandbox-api.md.
    3. **Implement MCP Client:** Create a helper function/class within the sandbox environment to easily make calls to the `CoreMCPServer` endpoint (provided via environment variable or context), handling MCP request/response formatting 01-core-framework.md.
    4. **Implement Basic JIT Runner Logic (Interpreter):** Add logic to the `/execute` handler to: receive `taskDetails` for a JIT task, load the specified script (using MCP `core.state.getDefinitionFileContent` [18, 7]), execute it using `subprocess` or equivalent, pass `requestData`/`context`, and return the result [10, 17].
    5. **Implement Basic LLM Runner Logic:** Add logic to the `/execute` handler to: receive `taskDetails` for an LLM task, get the prompt template (using MCP `core.state.getDefinitionFileContent` [18, 7]), render it with Jinja2 [9, 23], call the LLM (using MCP `core.llm.generate` [18, 7]), and return the result 03 - Core Framework Internal Components & APIs.md.

**Phase 4: Workflow & Prompt Definition/Execution**

- **Goal:** Define the schemas for application logic (workflows, prompts) and implement the workflow execution engine.
- **Tasks for Cline:**
    1. **Finalize Workflow YAML Schema:** Create a formal JSON Schema definition based on `05-workflow-yaml.md` [8, 21], ensuring it covers steps, types, transitions, error handling, etc.
    2. **Finalize Prompt Template YAML Schema:** Create a formal JSON Schema definition based on `06-prompt-template-yaml.md` [9, 23], covering metadata, parameters, template structure, etc.
    3. **Implement Workflow Execution Engine:** Within a sandbox type (e.g., `LLM Orchestrator/Runner` 03 - Core Framework Internal Components & APIs.md), implement the logic to parse a Workflow YAML (fetched via `core.state.getDefinitionFileContent` [18, 7]), execute steps sequentially based on `startAt` and `transitions`, handle different step types (`jit`, `llm`, `mcp`, `control` [8, 21]), manage step inputs/outputs, and implement basic error handling (`onFailure`, `onFailureDefault` [8, 21]). Requires testing 09-testing.md.

**Phase 5: Integration, Advanced Features & Polish (Iterative)**

- **Goal:** Integrate components, add optimization capabilities, build the UI, and strengthen security and testing.
- **Tasks for Cline (Examples):**
    1. **Implement `MetricCollector`:** Define and implement the API (Section 3.5 - spec needed) and storage mechanism [16, 22]. Integrate metric reporting calls in relevant framework/sandbox locations.
    2. **Implement `OptimizationOracle`:** Implement the basic logic based on Section 3.6 02 - Core Architecture.md and Section 7 08 - Prompt Template Format.md, including rule evaluation and triggering JIT generation.
    3. **Implement JIT Code Generation Flow:** Implement the process described in Section 7.3 07-jit-optimization.md: formulate spec, call Coder LLM via MCP 07-jit-optimization.md, store artifacts using `StateManagerInterface` 07-jit-optimization.md, update `ComponentRegistry` 07-jit-optimization.md.
    4. **Build Basic Admin Panel:** Create a simple web UI (potentially using an LLM for UI generation as per Section 9.1 01 - Concept Overview.md) for core tasks like application registration (interacting with `ApplicationRegistry` API [15, 24]).
    5. **Security Hardening:** Review `08-security.md` [11, 25] and implement specific controls (e.g., stricter input validation, permission checks using `ApplicationRegistry`, secure MCP tool execution 01-core-framework.md).
    6. **Develop Test Suites:** Create comprehensive integration tests 09-testing.md covering core workflows and end-to-end tests 09-testing.md for key application scenarios. Implement JIT test execution [10, 12].
    7. **Documentation Refinement:** Update all design docs and READMEs to reflect the final implementation details [1, 13].