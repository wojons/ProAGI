# UHLP Testing Standards (`09-testing.md`)

This document outlines the mandatory testing requirements and recommended strategies for the UHLP framework and applications developed using it. Comprehensive testing is essential for ensuring the stability, correctness, and security of this dynamic system.

## 1. Testing Philosophy

*   **Quality is Paramount:** Rigorous testing is not optional; it is a fundamental part of the development process.
*   **Early & Often:** Write tests alongside code. Integrate testing early into the development lifecycle and CI/CD pipelines.
*   **Multiple Layers:** Employ different types of testing (unit, integration, end-to-end) to cover various aspects of the system.
*   **Automation:** Automate tests whenever possible to ensure consistent and repeatable verification.

## 2. Core Framework Testing

*   **Unit Tests:** [1]
    *   **Scope:** Test individual functions, methods, and classes within Core Framework components (`ApplicationRegistry`, `SandboxManager`, `RequestRouter`, `StateManagerInterface`, etc.) in isolation.
    *   **Requirements:** Must cover core logic, edge cases, and expected error conditions. Aim for high code coverage (e.g., >80%) for critical components.
    *   **Mocking:** Extensively use mocking/stubbing libraries (e.g., Python's `unittest.mock`) to isolate the unit under test from its dependencies (other internal components, Docker API, external services).
    *   **Tools:** Use standard testing frameworks (e.g., `pytest` recommended for Python).
*   **Integration Tests:** [1]
    *   **Scope:** Test the interaction *between* Core Framework components. Examples:
        *   Verify `RequestRouter` correctly calls `ApplicationRegistry`, then `SandboxManager`, and dispatches to a mock sandbox.
        *   Verify `StateManagerInterface` correctly interacts with the underlying Git repository and/or Redis instance in a test environment.
        *   Verify `CoreMCPServer` routing logic and interaction with mock downstream MCP servers.
    *   **Environment:** Requires a more integrated environment than unit tests, potentially using test containers (e.g., via `testcontainers`) for dependencies like Redis or a local Docker daemon.
    *   **Focus:** Verify API contracts, data flow, and error handling between components.

## 3. Sandbox API (`/execute`) Testing

*   **Scope:** Test the HTTP server implementation running inside sandbox images, ensuring it correctly handles `/execute` requests according to the specification.
*   **Approach:** Build the sandbox Docker image. Run it as a container. Send test HTTP requests to its `/execute` endpoint covering various `requestData` and `context` scenarios. Assert the HTTP responses and JSON body (`resultType`, `data`, `metrics`) are correct.
*   **Mocking:** The sandbox container under test will likely need to mock its interactions with the MCP endpoint.

## 4. MCP Tool & Server Testing

*   **Tool Unit Tests:** Test the business logic of individual MCP tool implementations (e.g., the logic within `core.linux.executeCommand`'s whitelisting and wrapping) in isolation, mocking external dependencies.
*   **MCP Server Integration Tests:** Test the MCP server's HTTP handling, request parsing, authentication/authorization logic, tool dispatching, and routing to downstream servers (using mock downstream servers).

## 5. JIT Code Testing (CRITICAL)

*   **LLM Generates Tests:** The prompt used to generate JIT code via the "Coder LLM" **MUST explicitly require the generation of corresponding unit tests** (e.g., `pytest` format) alongside the functional code [1].
*   **Comprehensive Tests:** Generated tests **MUST** cover expected inputs, outputs, edge cases, and error handling defined in the JIT code specification provided to the Coder LLM.
*   **Execution Environment:** Tests **MUST** be designed to run within an environment that closely mimics the target JIT sandbox container, including access to necessary base libraries and potentially mocked MCP tools.
*   **Mandatory Execution:** A process **MUST** be established (CI/CD ideally, or pre-activation checks) to **automatically execute these generated tests** against the generated JIT code [1].
*   **Activation Gate:** Activation of newly generated JIT code (updating the `ComponentRegistry` state) **SHOULD ideally be blocked** if its corresponding tests fail.

## 6. Workflow YAML Testing

*   **Unit Testing (Difficult):** Unit testing individual steps within a complex YAML workflow declaratively is challenging. Focus more on integration testing.
*   **Integration/E2E Testing:** Test entire workflows by triggering them via their defined entry point (e.g., making an HTTP request to the trigger route).
    *   **Scope:** Verify the end-to-end flow, data transformations between steps, conditional logic branching, and final output.
    *   **Environment:** Requires a running UHLP framework instance (potentially scaled down) with mocked external dependencies (e.g., MCP tools connecting to external services).
    *   **Assertions:** Assert on the final output/response, and potentially on intermediate state changes or mock MCP call parameters if necessary for verification.

## 7. End-to-End (E2E) Testing

*   **Scope:** Simulate user interactions with a fully deployed UHLP application. Test critical user flows from the UI/API ingress point through the framework, sandboxes, MCP tools, and back [1].
*   **Tools:** May involve UI automation frameworks (e.g., Playwright, Selenium) or API testing tools.
*   **Focus:** Verify the overall application behavior and user experience. Target key use cases identified in the application definition.

## 8. Test Environments

*   **Local Development:** Developers should be able to run unit and relevant integration tests easily on their local machines.
*   **CI Environment:** The CI/CD pipeline needs environments capable of running unit tests, integration tests (potentially with service containers), and executing JIT tests.
*   **Staging Environment:** A dedicated staging environment closely resembling production is needed for running E2E tests and performing manual QA before deploying changes.

## 9. CI/CD Integration

*   **Automated Execution:** All automated tests (unit, integration, JIT tests) MUST be executed automatically in the CI pipeline on every commit/pull request.
*   **Build/Pipeline Failure:** The CI pipeline MUST fail if any tests fail, preventing merging of faulty code.
*   **Coverage Reporting:** Integrate code coverage reporting into the CI pipeline (optional but recommended).
