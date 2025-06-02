# Core Framework Development Standards (`01-core-framework.md`)

This document outlines the standards and guidelines for developing the **internal components** of the UHLP Core Framework (e.g., `ApplicationRegistry`, `SandboxManager`, `RequestRouter`, `StateManagerInterface`, `CoreMCPServer`, `MetricCollector`, `OptimizationOracle`). Adherence to these standards is crucial for maintainability, consistency, and stability.

## 1. Language & Environment

*   **Primary Language:** Python 3.11+
*   **Environment Management:** Use `venv` for virtual environments.
*   **Dependency Management:** Use `pip` with `requirements.txt` (or `pyproject.toml` with Poetry/PDM). Pin dependencies to specific versions. Avoid overly broad version specifiers. Add comments explaining the purpose of non-obvious dependencies.

## 2. Code Style & Formatting

*   **PEP 8:** Strictly adhere to PEP 8 guidelines.
*   **Formatter:** Use `black` for automatic code formatting. Ensure it's run before committing code.
*   **Linter:** Use `flake8` (with common plugins like `flake8-bugbear`, `flake8-comprehensions`) to catch style issues and potential bugs. Resolve all linter warnings.
*   **Imports:** Use `isort` to automatically sort imports. Group imports according to standard Python conventions (standard library, third-party, application-specific).
*   **Type Hinting:** Use Python type hints (`typing` module) for all function signatures, class attributes, and significant variable declarations. Use `mypy` in strict mode for static type checking.
*   **Naming Conventions:** Follow standard Python naming conventions (snake_case for variables/functions/methods, PascalCase for classes). Choose clear, descriptive names. Avoid single-letter variable names except in very small, obvious contexts (like loop counters).

## 3. Internal API Design (gRPC/HTTP)

*   **Primary Internal Protocol:** Use gRPC for inter-component communication within the Core Framework for type safety and performance. Define services and messages using Protocol Buffers (`.proto` files) [1].
*   **API Contracts:** Keep `.proto` definitions in a dedicated, shared location. Treat them as strict contracts. Changes require careful consideration of backward compatibility or versioning strategies.
*   **Error Handling:** Use standard gRPC status codes. Provide detailed error messages and potentially use `google.rpc.Status` with `google.rpc.ErrorInfo` for structured error reporting between services.
*   **Request/Response Naming:** Use consistent naming conventions (e.g., `ServiceNameRequest`, `ServiceNameResponse`).
*   **Idempotency:** Design API methods to be idempotent where appropriate, especially for state-changing operations.

## 4. Concurrency & Asynchronicity

*   **Asynchronous Framework:** Prefer asynchronous programming (`async`/`await`) for I/O-bound operations (network calls, file access via StateManager). Use libraries like `asyncio` and compatible frameworks (e.g., `aiohttp`, `asyncpg`).
*   **Avoid Blocking:** Do not block the main event loop with long-running synchronous or CPU-bound tasks. Offload CPU-bound work to separate processes or thread pools if necessary.
*   **Resource Management:** Use asynchronous context managers (`async with`) for managing resources like network connections or locks.

## 5. Error Handling & Logging

*   **Error Handling:**
    *   Use specific custom exception classes where appropriate to distinguish different error conditions within the framework.
    *   Do not swallow exceptions silently. Propagate them or handle them explicitly and log appropriately.
    *   Include relevant context in error messages.
*   **Logging:**
    *   Use structured logging (outputting logs as JSON). The standard library's `logging` module can be configured for this, or use libraries like `structlog`.
    *   **Mandatory Context:** All log messages MUST include standard context fields, such as: `timestamp`, `level`, `component_name`, `traceId` (if available), `appId` (if applicable), `requestId` (if applicable).
    *   Log meaningful messages at appropriate levels (`DEBUG` for detailed tracing, `INFO` for operational milestones, `WARN` for potential issues, `ERROR` for failures, `CRITICAL` for severe problems).
    *   Avoid logging sensitive information (API keys, passwords, raw user data) unless explicitly required and masked/anonymized appropriately.

## 6. Configuration

*   Use environment variables (potentially prefixed, e.g., `UHLP_CORE_DB_HOST`) as the primary method for configuring framework components.
*   Consider using a simple configuration file (e.g., YAML) for less sensitive or more complex default settings, which can be overridden by environment variables.
*   Avoid hardcoding configuration values (ports, endpoints, credentials) directly in the code.

## 7. Testing

*   **Unit Tests:** Write unit tests (`unittest` or `pytest`) for individual functions, methods, and classes. Aim for high code coverage. Mock external dependencies (other framework components, Docker API, StateManager backend).
*   **Integration Tests:** Write integration tests to verify the interaction *between* Core Framework components (e.g., `RequestRouter` correctly calls `SandboxManager` which interacts with Docker).
*   **Test Structure:** Organize tests logically, mirroring the application code structure.
*   **Fixtures:** Use fixtures (`pytest` fixtures recommended) for setting up test environments and dependencies.

## 8. Security

*   **Input Validation:** Validate all inputs received, even from other internal components. Assume inputs might be malformed or malicious.
*   **Least Privilege:** Design components to operate with the minimum necessary permissions.
*   **Dependency Security:** Regularly scan dependencies for known vulnerabilities (e.g., using `pip-audit` or similar tools).
*   **Principle Adherence:** Ensure implementations align with broader security principles defined in `08-security.md` (e.g., secure command execution if interacting with OS).

## 9. Documentation

*   **Docstrings:** Write clear docstrings for all public modules, classes, functions, and methods following PEP 257 (e.g., Google style or NumPy style). Explain the purpose, arguments, return values, and any potential exceptions raised.
*   **Code Comments:** Use inline comments sparingly to explain *why* something is done, not *what* is being done (the code should explain the what). Explain complex algorithms or non-obvious logic.