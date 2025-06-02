## 10. Security Considerations (Integrated & Future Work)

Security is a paramount concern in a dynamic system like UHLP, especially given its reliance on external models (LLMs), execution of dynamically generated code (JIT), and interaction with various external tools and data sources. This section outlines key security considerations integrated into the V0.1 design and highlights areas requiring ongoing attention or future enhancement.

### 10.1. Sandbox Isolation (Docker Dependency Isolation)

*   **V0.1 Approach (Docker):** The primary mechanism for isolating Sandboxed Components (JIT runners, LLM orchestrators) in V0.1 is Docker containers [1]. As stated in the UHLP Concept document (Section II), the main goal of this isolation is **dependency management and environment consistency**, preventing conflicts between different applications' libraries or runtime versions, akin to a Python `virtualenv` [1].
*   **Limitations:** While Docker provides process, filesystem, and network isolation through Linux namespaces and cgroups, it relies on a **shared host kernel** [2]. This means a critical kernel vulnerability could potentially allow escaping the container sandbox [2]. Therefore, Docker isolation in this context should **not** be considered a sufficient boundary against *intentionally malicious code* executing within the sandbox in high-security scenarios [1].
*   **Best Practices:** Standard Docker security practices are essential:
    *   Running processes inside containers as non-root users whenever possible.
    *   Using minimal base images.
    *   Applying resource limits (CPU, memory) via the `SandboxManager` to prevent denial-of-service [1].
    *   Restricting container capabilities.
    *   Configuring appropriate Docker network policies to limit inter-container communication.
*   **Future Work:** If requirements evolve to necessitate running truly untrusted code snippets or providing stronger multi-tenant isolation, migrating to technologies offering hardware-virtualized isolation like **Firecracker microVMs** [4] (as mentioned in Section VII of the UHLP document) should be evaluated [1].

### 10.2. Secured Command Execution (`core.linux.executeCommand`)

Executing arbitrary commands is inherently risky. The `core.linux.executeCommand` MCP tool, designed to provide access to essential utilities like `jq`, `curl`, `sed`, `awk`, MUST adhere to a strict security model as defined in the UHLP document (Section IV) [1] and specified for the `CoreMCPServer` (Section 5.4):

*   **Least Privilege:** Commands MUST execute under a dedicated, **low-privilege Linux user account** specific to UHLP sandbox operations, with minimal filesystem access [1].
*   **Strict Whitelisting:** Execution is restricted to commands explicitly listed on an **application-specific whitelist** [1]. This whitelist contains full paths to executables (e.g., `/usr/bin/jq`) and is managed via application configuration (`ApplicationRegistry`). Attempting to execute any command not precisely matching the whitelist MUST fail immediately [1]. Path manipulation must be prevented.
*   **Hardened Wrappers:** For necessary but potentially dangerous commands (`curl`, `sed`, `awk`), the system relies on **hardened wrapper scripts** [1]. These wrappers (generated during a secure development/testing phase involving security analysis) sanitize input arguments, enforce safe flags (e.g., preventing arbitrary URL schemes in `curl`, limiting regex complexity in `sed`/`awk`), and execute the underlying command with reduced risk [1]. The whitelist points to these wrappers, not the raw commands.
*   **No Shell Interpretation:** Command execution MUST avoid shell interpretation (e.g., using `shell=False` in Python `subprocess`) to prevent command injection vulnerabilities [1].
*   **Timeouts & Resource Limits:** Strict execution timeouts and, where possible, process-level resource limits (CPU, memory) MUST be applied to prevent runaway processes [1].

### 10.3. API Key Management (`ApplicationRegistry`, Validation)

Handling API keys for accessing external services (LLMs, Community MCP tools) or for authenticating clients to the UHLP application itself requires careful management:

*   **Secure Input:** Keys provided during application bootstrap (via Admin Panel) must be transmitted securely and handled carefully [1].
*   **Secure Storage:** Plaintext API keys **MUST NOT** be stored in version-controlled state (Git/YAML) or logs [1].
    *   For keys used by UHLP applications to authenticate *incoming* requests, they should be stored as secure, salted **hashes** (e.g., Argon2, bcrypt) within the `SecurityConfig` managed by the `ApplicationRegistry` [1]. The `ApplicationRegistryService.ValidateApiKey` method performs validation by hashing the incoming key and comparing it to the stored hash [1].
    *   For keys used by the framework/MCP servers to access *external* services (e.g., OpenAI API key), these should be managed through a secure secret management system (e.g., HashiCorp Vault, cloud provider secrets manager) and injected into the relevant MCP server containers (e.g., LLM Proxy or specific Community MCPs) as environment variables or mounted secrets, referenced via configuration rather than stored directly in `AppDefinition`.
*   **Validation:** The `ApplicationRegistryService.ValidateApiKey` provides a central point for validating incoming keys against stored hashes and retrieving associated application IDs and permissions [1].

### 10.4. Inter-App Communication Permissions (Framework Rules Needed)

If UHLP applications need to trigger events or call APIs in *other* UHLP applications hosted on the same framework instance (as discussed in Section 9), mechanisms are needed to control this:

*   **Policy Definition:** The `AppDefinition` (within `SecurityConfig`) should allow defining rules specifying which *source* application IDs (`allowedSourceAppId`) are permitted to trigger which specific events or routes (`allowedEvents`) in the *target* application [1].
*   **Framework Enforcement:** The `RequestRouter` or relevant event handling components within the Core Framework must consult these rules (via `ApplicationRegistryService`) before dispatching a trigger event from one application to another, rejecting unauthorized cross-app calls [1].

### 10.5. MCP Scoping & Permissions (App Context Enforcement)

The MCP architecture itself incorporates security scoping:

*   **App-Specific Context:** Communication between Sandboxes and MCP servers (especially `CoreMCPServer` and `AppSpecificMCPServer`) must securely identify the calling `appId` context [1]. This could involve trusting network identity within the Docker network (if strictly managed) or preferably using short-lived tokens injected into the sandbox `context`.
*   **Tool Authorization:** MCP Servers (`Core`, `AppSpecific`, `Community`) MUST authorize incoming tool requests based on the identified `appId`. They should consult the `ApplicationRegistry` or internal configuration to ensure the calling application is permitted to use the specific tool and potentially restrict parameters (e.g., ensuring `core.state.*` calls only access the calling `appId`'s state) [1].
*   **Credential Isolation:** Community MCP servers managing credentials for external services (like AWS, GDrive) must ensure strict isolation, only using the credentials configured specifically for the calling `appId` [1].

### 10.6. State Access Control (Via `StateManagerInterface`)

The `StateManagerInterface` acts as a gatekeeper for application state:

*   **`appId` Scoping:** All API methods (`GetDefinitionFileContent`, `ApplyDefinitionDiff`, `SetRuntimeValue`, etc.) require the `appId` as a parameter and MUST ensure operations are strictly confined to that application's designated state repository (Git path) or runtime namespace (Redis prefix) [1].
*   **Controlled Modifications:** Using `ApplyDefinitionDiff` with `expectedBaseRevision` provides optimistic concurrency control, helping prevent accidental overwrites or inconsistent state updates [1]. Access control for *who* can initiate state changes typically relies on authenticating the caller of the `StateManagerInterface` API (likely internal framework components or trusted processes).

### 10.7. Authentication & Authorization (User/Service)

*   **User Authentication:** The Core Framework needs integration with an authentication provider/mechanism to identify end-users interacting with UHLP applications. The user's identity (`userId`) and roles/permissions must be securely determined.
*   **Context Propagation:** Authenticated user information (`userInfo` including `id`, `roles`) must be securely propagated within the `context` object passed to sandboxes (`POST /execute`) [1].
*   **Authorization Checks:** Application logic within Sandboxes (LLM prompts, JIT code, workflow steps) can use the `context.userInfo` to perform fine-grained authorization checks before executing sensitive operations or returning data [1]. Roles and permissions can be defined in `SecurityConfig.userRoles` [1].
*   **Service Authentication:** Internal API calls between Core Framework components (gRPC) should ideally use service-to-service authentication mechanisms (e.g., mTLS).

### 10.8. Prompt Injection / LLM Security

Interacting with LLMs introduces unique security challenges:

*   **Prompt Injection:** Maliciously crafted inputs (potentially from end-users) could aim to manipulate the LLM's behavior by overriding original instructions within the prompt template. Careful input sanitization (where possible) and robust prompt design (e.g., using clear delimiters, strong system prompts, instructing the LLM to disregard conflicting user instructions) are necessary mitigation techniques.
*   **Data Exposure:** Ensure that prompts rendered via Jinja2 do not inadvertently include sensitive data from the context unless explicitly intended and authorized for the specific LLM interaction [2].
*   **Output Validation:** Using `outputFormat` and strict `outputSchema` validation on LLM responses helps mitigate risks from unexpected or malicious outputs generated by the LLM [2]. Sanitizing LLM outputs before they are used in subsequent steps (especially JIT execution or database queries) is crucial.

### 10.9. Secure Deployment

Beyond the application runtime, securing the deployment environment is critical:
*   Securing the host operating system where the framework and Docker run.
*   Implementing appropriate network firewall rules.
*   Securing access to the Docker socket used by the `SandboxManager`.
*   Protecting the Admin Panel with strong authentication and authorization.
*   Regularly updating framework components, language runtimes, and base Docker images.
*   Implementing robust logging and monitoring for security events.