# MCP Design & Implementation Standards (`04-mcp-design.md`)

This document outlines the standards for designing, implementing, and managing Model Context Protocol (MCP) tools and servers within the UHLP framework. Adherence ensures consistency, security, and interoperability across the ecosystem.

## 1. MCP Architecture Overview

*   **Purpose:** MCP provides a standardized interface for Sandboxed Components (JIT/LLM) to interact securely with framework capabilities, external services, data stores, and custom application logic [1].
*   **Interaction Model:** Sandboxes make HTTP POST requests to their designated `mcp_endpoint` (typically the App-Specific MCP Server or Core MCP Server) [1]. The request body specifies the `tool` name and `params`. The MCP server processes the request and returns a standard JSON response.
*   **Server Types & Scoping:** [1]
    *   **`CoreMCPServer`:** Implements fundamental framework tools (`core.*`). Shared resource, but access/routing considers the calling `appId`. Handles routing to other servers.
    *   **`AppSpecificMCPServer`:** Runs dedicatedly for each `appId`. Implements application-specific custom tools (`app.*`). Routes requests to Core and relevant Community servers. Acts as the primary endpoint for sandboxes within that `appId`.
    *   **`CommunityMCPServer`:** Provides reusable integrations for common services (e.g., AWS, GCP, specific databases, Stripe) (`community.*`). Instances may be scoped per `appId` if they manage app-specific credentials/configurations.
*   **Deployment:** MCP servers (except potentially Core in dev mode) SHOULD run as separate containers, managed potentially by the framework or deployed alongside applications [1].

## 2. Tool Design Principles

*   **Naming Convention:**
    *   Use a hierarchical, dot-separated format: `<namespace>.<subsystem>.<action>`.
    *   Namespaces: `core`, `community`, `app`.
    *   Choose clear, descriptive names for subsystems and actions (e.g., `core.state.getFileContent`, `community.aws.s3.putObject`, `app.reporting.generateDailySummary`).
*   **Granularity:** Design tools to perform specific, well-defined tasks. Avoid overly broad tools that perform too many unrelated actions. Compose complex operations using multiple tool calls within a workflow.
*   **Input (`params`):**
    *   Define a clear JSON schema for the `params` object expected by each tool. Use specific field names and data types (string, number, boolean, object, array).
    *   Validate inputs rigorously within the tool implementation. Assume inputs might be missing, malformed, or malicious.
*   **Output (Response `data`):**
    *   Define a clear JSON schema for the `data` object returned on successful execution.
    *   Return predictable structures.
*   **Idempotency:** Design tools to be idempotent whenever possible, especially for operations that modify state. If not idempotent, clearly document the side effects.
*   **Error Handling:**
    *   Return specific, documented error codes within the response body's `error` field (e.g., `{ "success": false, "error": { "code": "FILE_NOT_FOUND", "message": "..." } }`) for expected application-level errors (e.g., resource not found, validation failed).
    *   Allow transport-level errors (e.g., HTTP 500) only for unexpected internal server failures within the MCP server itself.

## 3. Implementation Standards (MCP Servers)

*   **Language:** While flexible, consistency within a server type (e.g., Core, specific Community servers) is preferred. Follow relevant coding standards (e.g., `01-core-framework.md` if using Python).
*   **HTTP Server:** Use lightweight, efficient HTTP frameworks. Implement the standard MCP request/response handling logic.
*   **Authentication & Authorization:**
    *   MCP servers MUST identify the calling `appId`. The exact mechanism (secure header injection, mTLS) needs framework-level definition.
    *   Servers (especially `CoreMCPServer` and shared Community servers) MUST verify that the identified `appId` is authorized to call the requested tool, potentially checking against rules defined in the `ApplicationRegistry` [1].
*   **Configuration:** Manage configuration (e.g., downstream service endpoints, credentials for Community servers) via environment variables or secure configuration management practices. Avoid hardcoding.
*   **Logging:** Use structured logging, including `appId`, requested `tool` name, outcome (success/failure), and duration for each call processed. Use the framework's standard logging practices [1].
*   **Testing:** Write unit tests for individual tool logic and integration tests for server request handling and routing.

## 4. Security Requirements for Tools

*   **Input Sanitization/Validation:** Sanitize and validate ALL parameters received in the `params` object before using them. Pay special attention to paths, SQL fragments, command arguments, URLs, etc.
*   **Least Privilege:** Implement tool logic to operate with the minimum necessary permissions. If interacting with external services, use scoped credentials.
*   **`core.linux.executeCommand`:** Implementations interacting with the OS (like the `CoreMCPServer`'s `executeCommand`) **MUST** strictly adhere to the defined security protocol: execute as low-privilege user, use exact-match whitelisting, employ hardened wrappers for risky commands, prevent shell injection, apply timeouts [1].
*   **Filesystem Access:** Tools accessing filesystems (like `core.filesystem.readFile`) **MUST** perform rigorous path validation, prevent directory traversal, and respect application-specific directory scopes [1].
*   **Credential Management:** Community/App servers managing credentials for external services MUST store and handle them securely (e.g., using environment variables, secrets management tools) and should ideally be scoped per `appId` to prevent cross-application credential exposure. Avoid returning raw credentials in tool responses.

## 5. Documentation

*   **Tool Definition:** Every MCP tool MUST be documented. This documentation should include:
    *   Full tool name.
    *   Clear description of its purpose.
    *   JSON schema for the input `params`.
    *   JSON schema for the output `data` on success.
    *   List of potential application-level error codes (`error.code`) and their meanings.
    *   Notes on idempotency, side effects, security considerations, or required permissions.
*   **Discovery:** Consider a mechanism (perhaps via `ApplicationRegistry` or a dedicated MCP discovery endpoint) for listing available tools and their schemas, aiding development and potentially LLM tool usage.
