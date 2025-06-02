# UHLP (Ultra High Level Programming) Framework Design Specification (V0.1 / "V0")

This document provides detailed specifications for the UHLP framework, based on the initial concept and subsequent design discussions.

## 1. Concept Overview (Reference: UHLP Document Section I)
    1.1. **Core Idea: LLM as Runtime**: UHLP elevates the programming abstraction where an LLM or AI acts as the core application runtime, interpreting high-level descriptions and orchestrating tasks [22].
    1.2. **Abstraction Layer**: Treats the LLM as the next-level execution layer beyond traditional VHLLs [22].
    1.3. **User Experience Analogy (Roblox-like)**: Aims to empower users to create applications via high-level descriptions and prompts [22].
    1.4. **JIT / Adaptive Nature (Predictive, Reactive, Optimizing)**: The system dynamically adapts, predicts needs, reacts to requests, and optimizes execution paths (LLM vs. JIT) based on performance and rules [22].

## 2. Core Architecture (Reference: UHLP Document Section II)
    2.1. **Immutable Core Framework Overview**: Provides the stable runtime environment, orchestration, monitoring, validation, state management APIs, and security enforcement [23].
    2.2. **Sandboxed Components Overview (Docker Containers)**: Isolated environments for dynamic logic execution [23].
        2.2.1. **Sandbox Types**: JIT Runners (Python, Node.js, etc.), LLM Orchestrators/Runners. Each application has its own dedicated pool(s) of sandboxes with specific dependencies installed [1, 24].
        2.2.2. **Execution Model (V0.1: Interpreter Mode for JIT)**: JIT code is executed via a simple runner process within the sandbox that invokes the target script file on-demand using the appropriate language interpreter [1]. No persistent application server (like FastAPI) within the JIT sandbox for V0.1 [1, 3, 4].
    2.3. **Interaction Model (Request Flow)**: User Request -> Ingress -> Core Framework (`RequestRouter`) -> `SandboxManager` (allocates instance) -> Sandbox (`/execute` call) -> [Sandbox Logic: LLM/JIT/Workflow -> MCP Calls -> Framework Tools/State/Other MCPs] -> Sandbox Response -> Core Framework -> User Response [23].
    2.4. **Core Framework -> Sandbox API Specification (Version 1.0)** [8]
        2.4.1. **Endpoint**: `POST /execute` (Internal API within the Sandbox container) [8]
        2.4.2. **Transport & Hosting**: HTTP/1.1 (Consider HTTP/2, HTTP/3 later). Sandbox runs a lightweight HTTP server on a designated port [8]. Core Framework (`RequestRouter` + `SandboxManager`) resolves the container's internal IP/hostname and port [8].
        2.4.3. **Request Structure**:
            *   **Headers**:
                *   `Content-Type: application/json` (Required) [8]
                *   `Accept: application/json` (Required) [8]
                *   `X-Request-ID: <uuid>` (Required - Framework invocation ID) [8]
                *   `X-Trace-ID: <uuid>` (Optional - End-to-end trace ID)
            *   **Body**: JSON payload:
                ```json
                {
                  "requestId": "string", // Matches X-Request-ID <source_id data="8" title="02-sandbox-api.md" />
                  "requestData": { // Details of the event triggering this execution <source_id data="8" title="02-sandbox-api.md" />
                    "source": "http" | "trigger" | "callback" | "queue" | "cron" | "internal", //<source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" /> Origin Type
                    // --- Conditional based on source ---
                    "httpDetails": { // Present if source == 'http' <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
                      "method": "GET" | "POST" | "PUT" | "DELETE" | "PATCH" | "OPTIONS" | "HEAD",
                      "path": "string", // e.g., "/api/users/123?param=value" (including query string)
                      "routePattern": "string", // e.g., "/api/user/:username" (Matched route, optional)
                      "pathParameters": { // Decoded path parameters based on routePattern (optional)
                         "username": "alice"
                      },
                      "queryParameters": { // Decoded query string parameters
                         "param": "value"
                      },
                      "headers": { // Key-value map of request headers
                        "Accept": "application/json",
                        "Authorization": "Bearer ..." // Passed through for sandbox handling if needed
                        /* ... other headers ... */
                      },
                      "body": "string", // Raw request body (Base64 encoded for binary data, plain string otherwise)
                      "bodyEncoding": "utf8" | "base64" // Indicates encoding of the body field
                    },
                    "triggerDetails": { // Present if source == 'trigger' <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
                       "sourceAppId": "string",
                       "triggerEvent": "string",
                       "payload": {} // JSON object payload specific to the trigger
                    },
                    "callbackDetails": { /* ... headers, body, etc. ... */ },
                    "queueDetails": { /* ... queueName, messageId, payload ... */ },
                    "cronDetails": { /* ... jobId, scheduledTime ... */ }
                  },
                  "context": { // Background information provided by the Framework <source_id data="8" title="02-sandbox-api.md" />
                    "appId": "string", // Unique ID of the UHLP application this request belongs to <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
                    "componentId": "string", // ID of the component/workflow being invoked (from state) [1, 25]
                    "mcp_endpoint": "string", // App-Specific MCP Server URL <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
                    "stateConfig": {
                        "type": "mcp_tool", // Assume state access is primarily via MCP tools initially
                        "readTool": "core.state.getFileContent",
                        "writeTool": "core.state.applyStateDiff" // Tools provided by Core MCP <source_id data="19" title="100 - Appendixes.md" />
                        // Could potentially support direct volume mounts later
                    },
                    "workflowInfo": { // Added if handlerType is WORKFLOW
                      "workflowId": "string", // From taskDetails
                      "startAt": "string" // Optional entry point override
                    },
                    "userInfo": { // Optional: Present if user context is available/authenticated <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
                      "id": "string",
                      "roles": ["string"],
                      "isAuthenticated": true,
                      "claims": {} // Optional: custom claims/attributes
                    },
                    "sessionId": "string", // Optional: Identifier for framework-managed session state [1, 25]
                    "configuration": { /* Injected app config values */ <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" /> },
                    "applicationInfo": { // General info about the running app <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
                        "deploymentMode": "production" | "development" | "staging"
                    }
                    // Avoid passing sensitive Framework internals directly; use MCP for access <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
                  }
                }
                ```
        2.4.4. **Response Structure**:
            *   **Success HTTP**: `200 OK` [8]
            *   **Failure HTTP**: `400` (Bad Request JSON), `500` (Sandbox Internal Error), `503` (Sandbox Unavailable), `429` (Optional: Overload). [8]
            *   **Headers**:
                *   `Content-Type: application/json` (Required on 200 OK) [8]
                *   `X-Request-ID: <uuid>` (Required - Echo request ID) [8]
            *   **Body (on 200 OK)**: JSON Payload:
                ```json
                {
                  "requestId": "string", // Matches request ID <source_id data="8" title="02-sandbox-api.md" />
                  "resultType": "generic" | "httpResponse" | "error" | "workflowStep", // Type of result <source_id data="8" title="02-sandbox-api.md" />
                  "data": {
                      // Type "generic": Raw data output. Example: { ... } [8, 1]
                      // Type "httpResponse": Defines full HTTP response. Example: { "statusCode": 200, "headers": {}, "body": "...", "bodyEncoding": "..." } [8, 1]
                      // Type "error": Application-level error. Example: { "code": "...", "message": "...", "details": {} } [8, 1]
                      // Type "workflowStep": Intermediate workflow result. Example: { "workflowId": "...", "stepId": "...", "status": "...", "output": {}, "error": {} } <source_id data="8" title="02-sandbox-api.md" />
                  },
                  "metrics": { // Optional sandbox metrics <source_id data="8" title="02-sandbox-api.md" />
                     "execution_time_ms": 123,
                     "mcp_calls": [ { "tool": "...", "count": 1, ... } ]
                     /* ... other metrics ... */
                  }
                }
                ```
            *   **Body (on 4xx/5xx)**: Optional JSON: `{ "error": "string", "details": "string" }`

## 3. Core Framework Internal Components & APIs [24]

### 3.1. `ApplicationRegistry` Internal API Specification (Version 1.0) [21, 24]
    3.1.1. **Purpose & Transport**: Central source of truth for app definitions, config, status, security. Transport: Internal gRPC. Service Name: `uhlp.framework.ApplicationRegistryService`. [20, 24]
    3.1.2. **Methods (Application Lifecycle & Management)**:
        *   `RegisterApplication(definition: AppDefinition) -> RegisterApplicationResponse { appId, success, error }` [16, 24]
        *   `UpdateApplication(appId: string, updates: AppDefinitionPatch) -> UpdateApplicationResponse { success, error }` [1]
        *   `DeregisterApplication(appId: string, deleteState: bool) -> DeregisterApplicationResponse { success, error }` [1]
        *   `GetApplicationStatus(appId: string) -> GetApplicationStatusResponse { appId, status: AppStatus, details }` [1]
        *   `ListActiveApplications() -> ListActiveApplicationsResponse { appIds: string[] }` [1] (Used by `SandboxManager`)
    3.1.3. **Methods (Configuration & Requirements Retrieval)**:
        *   `GetApplicationDetails(appId: string) -> GetApplicationDetailsResponse { definition: AppDefinition }` [1]
        *   `GetSandboxRequirements(appId: string) -> GetSandboxRequirementsResponse { appId, requirements: SandboxPoolConfig }` [1] (**Crucial for `SandboxManager`**)
        *   `GetComponentDefinition(appId: string, identifier: oneof { componentId | routeInput }) -> GetComponentDefinitionResponse { found, definition?, extractedPathParameters? }` [1, 25] (**Crucial for `RequestRouter`**)
        *   `GetAppConfigurationValue(appId: string, key: string) -> GetAppConfigurationValueResponse { key, found, value? }` [1]
    3.1.4. **Methods (Security & Permissions Information)**:
        *   `GetApplicationPermissions(appId: string) -> PermissionRules` (Structure TBD) [1]
        *   `ValidateApiKey(apiKey: string) -> ValidateApiKeyResponse { isValid, appId?, permissions? }` [1]
        *   `GetUserPermissionsForApp(appId: string, userId: string) -> string[]` (Structure TBD) [1]
    3.1.5. **Core Data Structures (Protobuf)**:
        ```protobuf
        message AppDefinition { string appId = 1; string displayName = 2; string version = 3; SandboxPoolConfig sandboxPools = 4; StateConfig stateStoreConfig = 5; ComponentRegistry initialComponentRegistry = 6; SecurityConfig securityConfig = 7; OptimizationConfig optimizationConfig = 8; } // Added OptConfig
        message SandboxPoolConfig { repeated PoolDefinition pools = 1; }
        message PoolDefinition { string poolName = 1; string dockerImage = 2; int32 minInstances = 3; int32 maxInstances = 4; ResourceLimits resourceLimits = 5; repeated string volumeMounts = 6;}
        message ResourceLimits { string cpuLimit = 1; string memoryLimit = 2; }
        message StateConfig { string type = 1; map<string, string> params = 2;} // e.g., type="git_yaml", params={"repoUrl": "..."}
        message ComponentRegistry { repeated ComponentDefinition components = 1; }
        message ComponentDefinition { string componentId = 1; HandlerType handlerType = 2; string targetPoolName = 3; map<string, string> taskDetails = 4; string expectedResultFormat = 5; RouteMatcher routeMatcher = 6; }
        enum HandlerType { HANDLER_TYPE_UNSPECIFIED = 0; HANDLER_TYPE_LLM = 1; HANDLER_TYPE_JIT = 2; HANDLER_TYPE_WORKFLOW = 3; }
        message RouteMatcher { string pathPattern = 1; repeated string methods = 2; }
        message SecurityConfig { repeated ApiKeyDefinition apiKeys = 1; repeated InterAppPermission interAppPermissions = 2;}
        message ApiKeyDefinition { string keyHash = 1; string description = 2; repeated string permissions = 3;}
        message InterAppPermission { string allowedSourceAppId = 1; repeated string allowedEvents = 2; }
        message OptimizationConfig { repeated OptRule rules = 1; bool preferLlmFlexibility = 2; } // Config for OptimizationOracle rules
        message OptRule { string scope = 1; /* GLOBAL, APP, COMPONENT */ string targetComponentId = 2; /* Optional */ string metric = 3; /* latency_ms, cost_usd, freq_per_min */ string condition = 4; /* >, <, == */ double threshold = 5; }
        // Include standard google.protobuf.Value for flexible config values
        ```

### 3.2. `SandboxManager` Specification (Version 1.0) [21]
    3.2.1. **Purpose & Responsibilities**: Manages lifecycle (creation, monitoring, destruction) of Docker Sandboxes based on `ApplicationRegistry` requirements. Ensures required pools are running for each application [21].
    3.2.2. **Discovery**: Polls `ApplicationRegistryService.ListActiveApplications()` and `ApplicationRegistryService.GetSandboxRequirements()` to get desired state [21, 1].
    3.2.3. **Docker Resource Management**: Interacts directly with Docker socket (`/var/run/docker.sock`) via Docker API to pull images, run/stop/remove containers, applying configs (limits, volumes) from `PoolDefinition` [21, 1].
    3.2.4. **Pool Management (Per-Application Pools)**: Maintains separate pools of containers for each active `appId` according to its specific `SandboxPoolConfig` [1]. Scales instances within `minInstances`/`maxInstances` bounds [24].
    3.2.5. **Health Monitoring & Recycling**: Checks container status via Docker API [21]. Optionally calls container internal health check endpoint (`GET /healthz`) [8]. Recycles unhealthy instances [21].
    3.2.6. **Instance Allocation API (Internal gRPC)**:
        *   `AllocateSandbox(appId: string, requiredPoolName: string) -> AllocateSandboxResponse { status: AllocationStatus, containerId?, networkAddress?, error? }` (Used by `RequestRouter`). Status: `ALLOCATED`, `NO_INSTANCE_AVAILABLE`, `POOL_NOT_FOUND` [1].
        *   Requires `ReleaseSandbox(containerId)` call or timeout/tracking mechanism (TBD V1 details) [23].

### 3.3. `StateManagerInterface` Internal API Specification (Version 1.0) [9, 21]
    3.3.1. **Purpose & Transport**: Unified internal API for framework/CoreMCP to interact with app state (Git/YAML definition + Redis runtime). Abstracts storage. Transport: Internal gRPC. Service Name: `uhlp.framework.StateManagerService` [9, 21]. Implicitly scoped by `appId` [1].
    3.3.2. **State Scopes**: Definition/Config (Git/YAML), Runtime (Redis) [1].
    3.3.3. **Definition State Methods (Git/YAML)**:
        *   `GetDefinitionFileContent(appId, filePath, revision?) -> { found, content, revision, error? }` [1, 19]
        *   `ApplyDefinitionDiff(appId, filePath, diffContent, expectedBaseRevision, commitMessage, author?) -> { success, resultingRevision, error? }` [1, 19] (Primary modification method). Handles locking, git commit [9].
        *   `SetDefinitionFileContent(appId, filePath, content, commitMessage, author?) -> { success, resultingRevision, error? }` [1, 19] (Overwrite/create) [9].
        *   `DeleteDefinitionFile(appId, filePath, commitMessage, author?) -> { success, resultingRevision, error? }` [1, 19]
        *   `ListDefinitionDirectory(appId, directoryPath, recursive, revision?) -> { entries: [{path, type}], revision, error? }` [1, 19]
    3.3.4. **Runtime State Methods (Redis)**:
        *   `SetRuntimeValue(appId, key, value: google.protobuf.Value, ttlSeconds?) -> { success, error? }` [1, 19, 9]
        *   `GetRuntimeValue(appId, key) -> { found, value?, error? }` [1, 19, 9]
        *   `DeleteRuntimeValue(appId, key) -> { success, error? }` [1, 19, 9]
        *   (Optional) `IncrementRuntimeValue`, `DecrementRuntimeValue`.

### 3.4. `RequestRouter` Specification (Version 1.1) [21]
    3.4.1. **Purpose & Hosting**: Central routing hub. Receives events (HTTP, triggers, etc.), determines target Sandbox (LLM/JIT/Workflow Orchestrator) via `ApplicationRegistry`, allocates via `SandboxManager`, constructs and dispatches `/execute` call, handles response. Runs in Core Framework [21, 1].
    3.4.2. **Input**: `appId`, `source`, `sourceDetails`, `traceId` [1].
    3.4.3. **Component/Workflow Identification**: Calls `ApplicationRegistryService.GetComponentDefinition` [1]. Checks `handlerType`. If `WORKFLOW`, gets `workflowId` from `taskDetails`. If `JIT`/`LLM`, gets specific `taskDetails` [1, 25]. Determines `targetPoolName` [1].
    3.4.4. **Sandbox Allocation**: Calls `SandboxManager.AllocateSandbox(appId, targetPoolName)` [23, 1].
    3.4.5. **`/execute` Request Construction**: Constructs JSON body including `requestData` (based on input `sourceDetails`), `context` (incl. `appId`, `componentId`, `mcp_endpoint`, retrieved `userInfo`, `sessionId`, relevant `configuration`, and `workflowInfo` if `handlerType` is `WORKFLOW`) [1, 23].
    3.4.6. **Sandbox Response Handling & Final Response Generation**: Makes `POST /execute` call [23]. Handles sandbox HTTP errors. On success (200 OK), parses sandbox JSON response, forwards `metrics` to `MetricCollector`. Processes `resultType` (`generic`, `httpResponse`, `error`, `workflowStep`) to construct appropriate final response [8, 23]. Calls `SandboxManager.ReleaseSandbox` if needed [23].

### 3.5. `MetricCollector` Specification (Version 1.0) [21]
    3.5.1. **Purpose & Hosting**: Aggregates and exposes operational metrics (performance, resource usage, custom). Source for monitoring. Runs in Core Framework (or separate container in Prod) [21, 1].
    3.5.2. **Input Interface**: Internal Push API (gRPC `RecordMetrics` or HTTP `POST /v1/metrics`). Receives metrics (e.g., from `RequestRouter` forwarding Sandbox metrics). Data model inspired by OpenTelemetry (OTLP) Metrics [`Metric`, `NumberDataPoint`, `HistogramDataPoint`] [19].
    3.5.3. **Key Attributes/Labels**: All metrics tagged with `appId`, `componentId`, `sandboxId`, `handlerType`, `poolName`, etc [1].
    3.5.4. **Output Interface**: HTTP `GET /metrics` endpoint exposing data in Prometheus Exposition Format for scraping [1].
    3.5.5. **Extensibility**: Handles arbitrary custom metric names (e.g., `app.custom.*`) pushed by components without prior collector configuration [1].

### 3.6. `OptimizationOracle` Specification (V0.2 - Enhanced Control) [21]
    3.6.1. **Purpose & Hosting**: Analyzes metrics (`MetricCollector`), identifies optimization opportunities (LLM -> JIT), initiates JIT generation based on configurable rules or manual triggers [22, 21]. Runs in Core Framework (background task).
    3.6.2. **Data Acquisition**: Periodically queries `MetricCollector` [21].
    3.6.3. **Decision Trigger**: Evaluates rules defined via `ApplicationRegistryService.GetApplicationDetails().definition.optimizationConfig` (Global, App, Component levels), considering thresholds (latency, cost, frequency) and flags (`preferLlmFlexibility`) [1]. Acts on rules or manual triggers [16]. May generate recommendations.
    3.6.4. **Manual Trigger Support**: API endpoint exposed (via Admin Panel integration) to force JIT generation for a component [16, 21].
    3.6.5. **JIT Process Initiation**: Formulates spec (inputs, outputs, language) based on current component definition (`StateManager`) [14]. Invokes Coder LLM via `core.llm.generate` MCP tool, requesting code and unit tests [14, 2]. Stores generated artifacts to versioned state (e.g., `_jit_code/...`) via `StateManagerService.SetDefinitionFileContent` [14].
    3.6.6. **Triggering State Update**: Calls `StateManagerService.ApplyDefinitionDiff` to update `ComponentRegistry` (change `handlerType` to `jit`, update `taskDetails` to point to new script) [14]. (No `HotReloadManager` needed for V0.1 Interpreter Mode) [1].

## 4. State Management Details (Reference: UHLP Document Section III) [9]
    4.1. **Conceptual Content**: `ApplicationDefinition`, `ComponentRegistry`, Prompts, Workflow YAMLs, JIT code artifacts, `RuntimeData`, etc [9, 25].
    4.2. **Storage Mechanisms**:
        4.2.1. **Definition/Config**: Git + YAML Files (Primary Source of Truth for versioned app definition). Managed via `StateManagerInterface` [9, 1].
        4.2.2. **Runtime Ephemeral State**: Redis (or similar key-value store). Managed via `StateManagerInterface` [1, 9].
        4.2.3. **Application Domain Data**: External Databases (e.g., Postgres via Supabase). Accessed via Community/App-Specific MCP servers, NOT `StateManagerInterface` [1].
    4.3. **Access API**: Exclusively via `StateManagerInterface` internal API (gRPC) [9].

## 5. Model Context Protocol (MCP) (Reference: UHLP Document Section IV) [10]
    5.1. **Role & Purpose**: Standardized interface (HTTP POST) for Sandboxes to interact securely with framework capabilities, external services, data stores, etc [10].
    5.2. **Multi-Server Architecture**: Core, App-Specific (dedicated per app), Community (pluggable, e.g., AWS, DBs). MCP Servers implemented with shared core code, deployed as separate containers (recommended) [20, 26, 1].
    5.3. **Scoping**: Core=Shared (but enforces permissions based on calling `appId`). App/Community=Logically scoped per-application. Sandbox connects to its App-Specific MCP, which routes requests onward [1].
    5.4. **`CoreMCPServer` Specification (Version 1.0)** [20, 26]
        5.4.1. **Purpose, Hosting, Transport**: Implements core framework tools, acts as gateway, routes to downstream MCPs. Runs as separate container. Transport: HTTP/1.1 (consider future upgrades) [20, 1].
        5.4.2. **Authentication/Authorization**: Must identify calling `appId` and validate tool permissions via `ApplicationRegistryService` [1].
        5.4.3. **Routing Logic**: Parses tool name (`core.*`, `community.*`, `app.*`), handles `core.*` locally, routes others to appropriate downstream MCP endpoint (lookup via `ApplicationRegistry`) [1].
        5.4.4. **V1 Core Toolset Implementation Details**:
            5.4.4.1. `core.framework.getConfigValue`: Wraps `ApplicationRegistryService`. Input: `{ key }`. Output: `{ found, value }` [19, 1].
            5.4.4.2. `core.framework.logFrameworkMessage`: Sends log to central logger. Input: `{ level, message, details? }`. Output: `{ success }` [19, 1].
            5.4.4.3. `core.state.*`: Wrappers for `StateManagerService` methods (GetDefFile, ApplyDefDiff, Set/Get/DeleteRuntimeValue, etc.). Inputs/Outputs match StateManager API [19, 1].
            5.4.4.4. `core.llm.generate`: Standardized LLM invocation. Routes to configured provider (OpenAI, Anthropic, Ollama proxy) based on `appId` config from `ApplicationRegistry`. Input: `{ model?, prompt, parameters? }`. Output: `{ success, completion, usage, error? }` [19, 1].
            5.4.4.5. `core.linux.executeCommand`: Secure execution. Input: `{ command, arguments, stdin?, timeoutSeconds? }`. Output: `{ success, exitCode, stdout, stderr, error? }` [19, 1]. **Implementation MUST:** run as low-priv user, check `command` against `appId`-specific whitelist (full paths only), execute hardened wrappers for risky tools (curl, sed, awk, jq, csvsql), prevent path traversal/shell injection, enforce timeouts [26, 1, 3].
            5.4.4.6. `core.filesystem.*` (Optional V1): `readFile`, `writeFile`. Input: `{ filePath }`, `{ filePath, content }`. Output: `{ success, content?, error? }` [19, 1]. **Implementation MUST:** validate path confinement to app-specific shared volumes, prevent traversal [26].

## 6. Workflow Definition [11]

### 6.1. Workflow YAML Structure Specification (Version 1.0) [13]
        6.1.1. **Purpose & File Location**: Declarative definition for multi-step processes. Stored in app state (e.g., `workflows/workflow_id.yaml`). Interpreted by orchestrator sandbox (LLM or JIT runner) [11, 13].
        6.1.2. **Top-Level Properties**:
            *   `workflowId: string` (Unique ID) [11]
            *   `description: string` (Optional) [11]
            *   `trigger: { type: string, config: object }` (Defines initiation event/route) [11]
            *   `startAt: string` (ID of the first step) [11]
            *   `steps: { <stepId>: StepDefinition, ... }` (Map of steps) [11]
        6.1.3. **Step Definition (`StepDefinition`)**:
            *   `type: "jit" | "llm" | "mcp" | "control"` [1]
            *   `description: string` (Optional)
            *   `target: object` (Details based on type: language/script/function for `jit`; promptTemplate/model for `llm`; tool name for `mcp`) [1]
            *   `inputMapping: object` (Maps workflow data to step inputs using Expression Syntax) [1]
            *   `transitions: object | array` (Defines next steps based on conditions or success/failure) [1]
            *   `subtype: string` (For `control` type, e.g., `formatResponse`) [11]
            *   `retryPolicy: object` (Optional: Define retries on failure)
        6.1.4. **Step Types**: `jit` (triggers JIT execution via MCP), `llm` (calls LLM via MCP), `mcp` (calls MCP tool directly), `control` (internal logic, e.g., `formatResponse`) [11, 1].
        6.1.5. **Expression Syntax (V1)**: Dot notation for accessing `trigger.*`, `steps.<stepId>.output.*`, `step.output.*`, `workflow.*`, `context.*`. String literals (`'literal'`), basic comparisons (`==`, `!=`, `>`, etc.), logical operators (`&&`, `||`, `!`), `defined()` check [13, 1].
        6.1.6. **Transitions & Flow Control**: `onSuccess`, `onFailureDefault`, conditional `transitions` array (`{ condition: expression, nextStep: stepId }`), `end: true` for terminal steps [11, 1].
    6.2. **Enhancements Inspired by n8n (Placeholders for V2)**: Dedicated structures/steps for Looping (`loop`), Merging/Splitting (`branch`, `merge`), Waiting (`wait`), Subworkflows (`subworkflow`), advanced Error Handling (`catch`) [13, 1].

## 7. Dynamic Execution & Optimization (Reference: UHLP Document Section V)
    7.1. **Runtime Decision Making**: Handled by `OptimizationOracle` based on metrics and configured rules [22].
    7.2. **Execution Paths**: LLM interpretation vs. JIT code execution [22].
    7.3. **JIT Code Generation Workflow**: Orchestrated by `OptimizationOracle` (Spec -> Coder LLM -> Store Artifacts -> Update State) [14, 22].
    7.4. **Multi-Layer Caching**: Concept noted, details TBD for V1 [14].

## 8. Prompt Template Format [12, 21]

### 8.1. LLM Prompt Template Format Specification (Version 1.0) [15, 21]
        8.1.1. **Purpose & File Format**: Standard structure for LLM prompts in app state (e.g., `prompts/prompt_name.yaml`). YAML format [15, 12].
        8.1.2. **Structure**:
            ```yaml
            description: Optional string [12, 15]
            model: Optional string (override app default) <source_id data="12" title="06-prompt-templates.md" />
            parameters: Optional object (default LLM params) <source_id data="12" title="06-prompt-templates.md" />
            template: | Required string (Jinja2 templating enabled, supports Markdown) [15, 1]
            outputFormat: Optional string ("json", "text", etc.) [21, 1]
            outputSchema: Optional object (JSON Schema for validation) [21, 1]
            # examples: Optional list (For few-shot, TBD structure V2+) <source_id data="15" title="08 - Prompt Template Format.md" />
            ```
        8.1.3. **Templating Engine**: Jinja2 (`{{ variable }}`, `{% if %}`, `{% for %}`, filters) [15, 1]. Context provided via workflow `inputMapping` [1].
        8.1.4. **Output Specification**: `outputFormat` hints, `outputSchema` validates structured responses [21, 1].

## 9. UI & Application Lifecycle (Reference: UHLP Document Section VI & VII) [21]
    9.1. **UI Generation**: V1 assumes LLM generates HTML/CSS/JS served by Core Framework [16, 21]. Details TBD.
    9.2. **Bootstrap Process**: User defines app via Admin Panel, triggers `ApplicationRegistry.RegisterApplication` which sets up initial state/config [16, 21].
    9.3. **Deployment**: Framework manages shareable subdomain and basic access control [21].
    9.4. **Admin Panel Requirements (V1 Sketch)**: Basic UI for `ApplicationRegistry` functions (Register/Update/Deregister, Status), viewing metrics (via `MetricCollector`), configuring optimization rules [16, 21]. Design TBD.

## 10. Security Considerations (Integrated & Future Work) [17]
    10.1. **Sandbox Isolation**: Docker provides process/dependency isolation [3, 17]. Not a hardened security boundary for malicious code in V1 [17].
    10.2. **Secured Command Execution**: `core.linux.executeCommand` enforces whitelist, low-priv user, hardened wrappers [26, 1].
    10.3. **API Key Management**: `ApplicationRegistry` stores hashes, provides `ValidateApiKey`. Applications access external keys securely (likely via configuration accessed through `core.framework.getConfigValue`) [3, 1].
    10.4. **Inter-App Communication Permissions**: Rules defined in `AppDefinition.SecurityConfig`, enforced by Framework (likely `RequestRouter` or event bus) [3, 1].
    10.5. **MCP Scoping & Permissions**: Core MCP enforces tool access based on calling `appId`. App/Community MCPs inherently scoped [1].
    10.6. **State Access Control**: All state access MUST go through `StateManagerInterface` (or its Core MCP wrappers) [3].
    10.7. **Dependency Scanning:** Use tools like `pip-audit` in CI/CD [3, 7].
    10.8. **Secrets Management:** Use env vars or secrets manager, NEVER hardcode secrets [9, 3].
    10.9. Secure Deployment: Host security, network firewalls, secure Docker socket, Admin Panel auth, regular updates [17].

## 11. Future Work / V2+ Considerations [18, 19]
    11.1. Advanced Optimization Logic (ML Models, Dynamic Rollback, A/B testing) [18].
    11.2. Enhanced Workflow Capabilities (Looping, Merging, Subworkflows, Waiting, Error Handling based on n8n inspiration) [13, 18, 19].
    11.3. HTTP/2 & HTTP/3 Support for internal/external APIs [1].
    11.4. Multi-Host Scaling (`SandboxManager`, Framework Clustering, distributed state considerations) [19, 1].
    11.5. LLM-Generated Grafana Dashboard Configuration [18, 4].
    11.6. Advanced Caching Strategies [14].
    11.7. JIT Server Mode Execution with Hot Reloading (if Interpreter Mode proves insufficient) [1, 18].
    11.8. Dedicated Debugging/Observability Tooling for tracing UHLP flows visually [18].
    11.9. Explicit definition of App-Specific / Community MCP server interfaces and discovery.
    11.10. Detailed specification of Admin Panel UI/features [16, 18].
    11.11. Refined security mechanisms (e.g., secure token passing between components, stronger sandbox isolation like Firecracker [17]).
    11.12 Advanced State Consistency mechanisms [18].

## 12. Development & Documentation Standards (Meta)
    12.1. **Language & Environment**: Python 3.11+, `venv`, `pip`/`requirements.txt` or Poetry/PDM [7].
    12.2. **Code Style**: PEP 8 (using Black, Flake8, isort) [7].
    12.3. **Testing Philosophy:** Quality paramount, early & often, multiple layers (unit, integration, E2E), automation. CI pipeline MUST fail on test failures [4, 1].
    12.4. **Core Framework Testing:** Unit tests for modules, integration tests for API boundaries [4].
    12.5. **JIT Code Testing:** Mandatory unit tests generated alongside JIT code by Coder LLM [2]. Execution of these tests (potentially manual V1, automated later) required before activation [2].
    12.6. **E2E Testing:** Simulate key user flows through the deployed system [4].
    12.7. **Documentation Requirements:** Docstrings (PEP 257), code comments for 'why', update `/docs` on changes, README, CHANGELOG, ADRs for major decisions [1, 7, 5]. Accuracy is critical [5]. OpenAPI Specs for external APIs [5].