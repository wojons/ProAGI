## 5. Model Context Protocol (MCP) (Reference: UHLP Document Section IV)

The Model Context Protocol (MCP) is a crucial standardization layer within the UHLP framework, defining how Sandboxed Components (LLM runners, JIT code, workflow orchestrators) interact with the capabilities provided by the Core Framework, external tools, data sources, and other services in a consistent and secure manner [1].

### 5.1. Role & Purpose

MCP serves as a **unified interface or API standard** enabling sandboxed logic to request actions or information from its surrounding environment [1]. Instead of allowing sandboxes to make arbitrary network calls or directly access host resources, they are expected to interact primarily through well-defined MCP "tool calls" [1].

The key purposes of MCP are:
*   **Abstraction:** Hides the implementation details of how a capability is provided (e.g., whether state is read from Git or Redis, whether an LLM call goes to OpenAI or Ollama) [1]. The sandbox invokes a standard tool (e.g., `core.state.getFileContent`, `core.llm.generate`) regardless of the backend [1].
*   **Standardization:** Provides a consistent way for LLMs and JIT code to request common functionalities like state access, configuration reading, logging, command execution, database interaction, etc. [1].
*   **Security & Control:** Creates a controlled gateway for sandbox interactions. The MCP server layer can enforce permissions, validate requests, apply rate limiting, and ensure operations like command execution occur within defined security boundaries [1].
*   **Extensibility:** Allows new tools and integrations (e.g., for specific databases, external APIs like Stripe or GDrive, custom application functions) to be added systematically by implementing them as distinct MCP servers or toolsets [1].

Sandboxes are typically provided with a single `mcp_endpoint` URL (within their execution `context`) which points to their primary MCP gateway (usually the Application-Specific MCP Server or the Core MCP Server) [1]. All tool calls are directed to this endpoint.

### 5.2. Multi-Server Architecture (Core, App-Specific, Community)

To manage complexity and scope, the MCP implementation utilizes a multi-server architecture:

*   **`CoreMCPServer`:** This server provides the foundational tools intrinsically linked to the Core Framework's capabilities [1]. This includes access to framework configuration, state management wrappers (`core.state.*`), generic LLM invocation (`core.llm.generate`), secure command execution (`core.linux.executeCommand`), logging (`core.framework.logFrameworkMessage`), etc. [1]. It also acts as the central router for tool calls destined for other MCP servers [1]. While potentially integrated in dev mode, it typically runs as a **separate container** in production, closely associated with the Core Framework deployment [1].
*   **`AppSpecificMCPServer`:** Each deployed UHLP application has its own dedicated instance (or pool) of an Application-Specific MCP Server [1]. The Sandbox instances for that application primarily communicate with this server [1]. Its role is to:
    *   Implement **custom tools or functions** defined specifically for *that* application [1].
    *   Authenticate/authorize requests based on the application context [1].
    *   Intelligently **route** requests for core, community, or its own tools to the appropriate destination [1] (i.e., it calls the `CoreMCPServer` for `core.*` tools, relevant Community servers for `community.*` tools, and handles `app.*` tools itself).
*   **`CommunityMCPServer`:** These are pluggable, often pre-built servers providing standardized tools for common external services or databases [1]. Examples include servers for interacting with AWS services (S3, DynamoDB), Google Drive, Stripe, specific SQL/NoSQL databases (Postgres, MongoDB), email services (SendGrid), etc. [1]. Each application needing such a service would typically have a configured (and potentially isolated) instance or endpoint for the relevant Community MCP server, likely routed via its `AppSpecificMCPServer` or the `CoreMCPServer` [1].

### 5.3. Scoping (Core=Shared, App/Community=Per-Application)

*   **Core:** The functionality provided by the `CoreMCPServer` (state access, config, logging, secured command execution) is generally shared infrastructure available to all applications, although authorization ensures an application can only access *its own* state and configuration [1].
*   **App-Specific/Community:** Tools implemented by `AppSpecificMCPServer`s or accessed via `CommunityMCPServer`s are typically **scoped per application** [1]. The routing layer (`CoreMCPServer` or `AppSpecificMCPServer`) ensures that a request originating from App "A" is directed to the Community/App-Specific MCP instance configured for App "A" (e.g., using App "A"'s database credentials or custom functions) [1]. This prevents App "A" from accidentally (or maliciously) invoking tools or accessing data scoped to App "B" [1].

### 5.4. `CoreMCPServer` Specification (Summary - See Section 3.5 for full details)

This is the foundational MCP server implementation.

*   **Purpose:** Implements core framework tools and routes other requests [1].
*   **Hosting:** Typically a separate container, associated with the Core Framework deployment [1].
*   **Transport:** HTTP/1.1 (V1 target) [1].
*   **Authentication/Authorization:** Must identify the calling `appId` and verify its permission to use the requested `core.*` tool, potentially consulting `ApplicationRegistryService` [1].
*   **Routing Logic:** Handles requests prefixed with `core.*` locally. For other prefixes (`community.*`, `app.*`), it looks up the appropriate downstream MCP server endpoint (based on calling `appId` and configuration from `ApplicationRegistry`) and forwards the request [1].
*   **V1 Core Toolset Implementation:**
    *   `core.framework.getConfigValue`: Reads app configuration via `ApplicationRegistryService` [1].
    *   `core.framework.logFrameworkMessage`: Logs messages centrally [1].
    *   `core.state.*`: Wrappers for `StateManagerInterface` methods (Get/ApplyDiff/Set/Delete DefinitionFileContent, Set/Get/Delete RuntimeValue) enforcing `appId` scope [1].
    *   `core.llm.generate`: Standardized LLM invocation, routing to configured provider (OpenAI, Ollama, etc.) via `ApplicationRegistry` lookup [1].
    *   `core.linux.executeCommand`: **Securely** executes commands [1]. **Crucially**, this implementation MUST:
        1.  Run the command as a dedicated, low-privilege user [1].
        2.  Consult an application-specific **whitelist** of allowed command paths (e.g., `/usr/bin/jq`, `/usr/local/bin/curl-wrapper`) [1]. Reject unknown commands immediately.
        3.  Execute **hardened wrapper scripts** for potentially risky but necessary tools (like `curl`, `awk`, `sed`), where the wrappers enforce safe arguments and flags [1]. These wrappers are generated based on security review during development/testing [1].
        4.  Execute safe, whitelisted commands directly, preventing shell interpretation [1].
        5.  Apply strict timeouts and capture `stdout`, `stderr`, `exitCode` [1].
        6.  Apply resource limits (CPU, memory) if possible [1].
    *   `core.filesystem.*` (Optional V1): Read/write files on shared volumes, requiring rigorous path validation and permission checks relative to the application's allowed directories [1].

### 5.5. Non-Core Routing Example

Illustrates how the `CoreMCPServer` (or potentially the `AppSpecificMCPServer` acting as primary gateway) routes calls:

1.  Sandbox for App "Blog" needs to put an object in S3. It calls its `mcp_endpoint` requesting the tool `community.aws.s3.putObject` with specific parameters (bucket, key, data).
2.  The receiving MCP server (assume `CoreMCPServer` for this example) parses the tool name. It sees the `community.aws.s3` prefix.
3.  It identifies the calling application as "Blog".
4.  It consults its routing configuration (derived from `ApplicationRegistry` for "Blog") to find the network address of the AWS S3 Community MCP Server instance specifically configured for "Blog" (which holds or accesses "Blog"'s AWS credentials securely).
5.  It forwards the essential request details (tool: `putObject`, parameters: `{bucket, key, data}`) to that target Community MCP server instance.
6.  The Community MCP server performs the S3 operation using "Blog"'s credentials.
7.  The Community MCP server sends the result (success/failure, metadata) back to the `CoreMCPServer`.
8.  The `CoreMCPServer` relays this result back to the original Sandbox that made the call.

### 5.6. Modular Design

The MCP servers (`Core`, `AppSpecific`, `Community`) can share a common core codebase responsible for handling the MCP protocol itself (parsing requests, formatting responses, basic routing logic) [1]. Specific tool functionalities are implemented as pluggable modules, allowing different server deployments to bundle only the modules they need [1].