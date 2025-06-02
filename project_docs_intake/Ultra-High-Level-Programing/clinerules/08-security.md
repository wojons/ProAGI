# UHLP Security Guidelines (`08-security.md`)

This document outlines mandatory security principles and specific requirements for developing and operating the UHLP framework and applications. Security must be a primary consideration at all stages of design and implementation.

## 1. Core Principles

*   **Defense in Depth:** Employ multiple layers of security controls. Do not rely on a single mechanism.
*   **Least Privilege:** Components (framework modules, sandboxes, MCP tools) MUST operate with the minimum permissions necessary to perform their function.
*   **Secure by Default:** Design components and configurations to be secure by default. Opt-in for less secure behavior only when explicitly necessary and justified.
*   **Input Validation:** Treat all external inputs and data crossing trust boundaries (including internal API calls between components) as potentially malicious. Validate rigorously.
*   **Secure Dependencies:** Keep all software dependencies (framework, sandboxes, libraries) updated and regularly scanned for known vulnerabilities.

## 2. Sandboxing (Docker)

*   **Primary Purpose (V1):** Recognize that Docker sandboxes in V1 primarily provide **dependency and environment isolation**, not a robust security boundary against intentionally malicious code execution within the sandbox [1]. Stronger mechanisms (like Firecracker) are future considerations [1].
*   **Resource Limits:** `SandboxManager` MUST apply strict CPU and memory limits when creating sandbox containers to prevent resource exhaustion attacks [1].
*   **Network Isolation:** Configure Docker networking to limit communication. Sandboxes should typically only need to communicate with their designated MCP endpoint and potentially other specific, required internal services. Avoid exposing unnecessary ports.
*   **Read-only Filesystem:** Where possible, configure sandbox containers to use a read-only root filesystem, mounting necessary writeable paths explicitly as volumes (e.g., for temporary files).

## 3. Model Context Protocol (MCP) Security

*   **Authentication & Authorization:**
    *   MCP Servers **MUST** reliably identify the source `appId` of incoming requests [1]. The mechanism (e.g., mTLS, secure token injection) MUST be robust.
    *   MCP Servers **MUST** authorize requests based on the `appId`, ensuring App A cannot execute tools intended only for App B or access restricted `core` tools [1]. Consult `ApplicationRegistry` for permissions.
*   **Tool Input Validation:** Every MCP tool implementation **MUST** rigorously validate and sanitize its input `params` *before* using them [1]. Pay extreme attention to parameters used in file paths, database queries, command execution, or network requests.
*   **`core.linux.executeCommand`:** [1]
    *   **STRICTLY MANDATORY:** Adhere *exactly* to the defined security protocol: execute as a dedicated low-privilege user, use exact-match command whitelisting (per `appId`), generate and use hardened wrappers for risky commands (`curl`, `sed`, etc.), prevent shell injection, enforce timeouts.
*   **`core.filesystem.*`:** [1]
    *   **STRICTLY MANDATORY:** Implement rigorous path validation, enforce application-specific directory scoping configured via `ApplicationRegistry`, and absolutely prevent directory traversal (`../`).
*   **Credential Handling:** [1]
    *   Community/App MCP Servers managing external credentials **MUST** store them securely (secrets management, environment variables) and scope them per `appId`.
    *   **NEVER** return raw credentials or sensitive configuration in MCP responses.

## 4. State Management Security

*   **No Secrets:** **NEVER** store secrets (API keys, passwords, credentials, PII) in the Git/YAML definition state [1]. Use secure configuration injection (env vars) or dedicated secrets management.
*   **Controlled Access:** Access state **ONLY** via the `StateManagerInterface` and its MCP wrappers (`core.state.*`) [1]. Protect the `StateManagerInterface` API itself.
*   **Authorization on Write:** `StateManagerInterface` (specifically `ApplyDefinitionDiff`, `SetDefinitionFileContent`, `DeleteDefinitionFile`) **MUST** authorize modification requests based on the calling context (e.g., ensuring only authorized framework components like `OptimizationOracle` or Admin API handlers can commit changes).

## 5. Application & API Security

*   **Ingress Validation:** The initial point of entry into the Core Framework (e.g., `RequestIngestor`) **MUST** perform basic input validation on incoming HTTP requests (e.g., request size limits, basic header checks).
*   **API Key Management:** [1]
    *   Store API key hashes securely (via `ApplicationRegistry`).
    *   Implement robust API key validation (`ValidateApiKey`).
    *   Associate keys clearly with specific applications (`appId`) and granular permissions.
*   **Inter-App Communication:** The framework **MUST** enforce configured rules governing which applications can trigger events or make requests to other applications [1].
*   **Permissions Checks:** Workflow logic and component implementations **MUST** explicitly check user/API key permissions (obtained from the `context` object or via MCP calls) before performing sensitive actions.

## 6. JIT Code Security

*   **Code Review:** Strongly recommend implementing a process for reviewing JIT code generated by LLMs, especially for security-sensitive components, before it's activated [1].
*   **Testing:** Ensure generated unit tests are executed and pass before activating JIT code. Tests should cover security aspects like input validation [1].
*   **Limited Scope:** JIT code runs within the potentially limited security boundary of the Docker sandbox. It relies heavily on MCP for secure resource access [1]. Avoid granting JIT code direct access to sensitive host resources.

## 7. LLM Interaction Security

*   **Prompt Injection:** [1]
    *   Design prompts to clearly separate trusted instructions from potentially untrusted user input (use delimiters, specific formatting).
    *   Sanitize or validate user input *before* inserting it into prompts where possible.
*   **Output Validation:** Use `outputSchema` validation whenever receiving structured data (especially JSON) from LLMs to prevent unexpected formats or injection into downstream processing [2].
*   **Data Minimization:** Only include sensitive data in prompts when absolutely necessary for the task. Avoid sending unnecessary PII or secrets to LLMs.

## 8. Dependency Management

*   **Regular Scanning:** Implement automated scanning (e.g., in CI/CD pipelines) for known vulnerabilities in ALL dependencies (Core Framework, Sandbox base images, libraries used in JIT code). Use tools like `pip-audit`, `npm audit`, `snyk`, etc.
*   **Prompt Updates:** Maintain a process for promptly updating dependencies when critical vulnerabilities are found.

## 9. Configuration & Secrets

*   **Secure Injection:** Use environment variables or a dedicated secrets management system (like HashiCorp Vault, AWS Secrets Manager) to inject secrets and sensitive configuration into the Core Framework and potentially MCP servers.
*   **Avoid Hardcoding:** **NEVER** hardcode secrets, API keys, or credentials in source code, configuration files (including state YAML), or container images.
