## 3. Core Framework Internal Components & APIs

This section provides detailed specifications for the primary internal software components that constitute the UHLP Core Framework. These components collaborate to manage applications, orchestrate execution within sandboxes, handle state, collect metrics, and perform optimizations. Each component typically exposes an internal API (often gRPC for efficiency and type safety within the framework cluster) for interacting with other core components [1].

### 3.1. `ApplicationRegistry` Internal API Specification (Version 1.0)

#### 3.1.1. Purpose & Transport (gRPC)

The `ApplicationRegistry` serves as the central nervous system and source of truth for managing the lifecycle, definition, configuration, and security context of all UHLP applications hosted by the framework instance [1]. It persists application definitions (potentially caching them from the primary Git/YAML state store [1] or managing their registration) and exposes a queryable interface for other components [1]. It is the authoritative source for information required by the `SandboxManager` to provision resources, the `RequestRouter` to make routing decisions, and MCP servers to enforce permissions and find configurations [1].

**Transport Protocol:** Internal gRPC is preferred for efficient, strongly-typed communication between core framework services [1].

**Service Name:** `uhlp.framework.ApplicationRegistryService`

#### 3.1.2. Methods (Application Lifecycle & Management)

These methods handle the creation, modification, and removal of applications within the framework's purview.

*   **`RegisterApplication`**
    *   **Purpose:** Registers a new UHLP application, making it known to the framework and initiating resource provisioning (via interaction with `SandboxManager`). Typically called during the application bootstrap process initiated via the Admin Panel [1].
    *   **Request:** `RegisterApplicationRequest`
        ```protobuf
        message RegisterApplicationRequest {
          AppDefinition definition = 1; // Full application definition, likely sourced from initial user input/config files.
        }
        // --- AppDefinition Structure ---
        // Defines the entire application: ID, metadata, sandbox needs, state config,
        // initial components/routes, security rules etc.
        message AppDefinition {
            string appId = 1; // User-provided or framework-generated unique ID
            string displayName = 2;
            string version = 3;
            SandboxPoolConfig sandboxPools = 4; // Requirements for the Sandbox Manager <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
            StateConfig stateStoreConfig = 5; // How state is stored (e.g., Git repo path) <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
            ComponentRegistry initialComponentRegistry = 6; // Map of routes/components to handlers <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
            SecurityConfig securityConfig = 7; // API Keys, inter-app permissions <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
            map<string, google.protobuf.Value> configuration = 8; // Default app-level config values
            OptimizationConfig optimizationConfig = 9; // Rules for OptimizationOracle
            // ... other metadata ...
        }
        // --- Supporting Structures for AppDefinition ---
        message SandboxPoolConfig { repeated PoolDefinition pools = 1; }
        message PoolDefinition {
          string poolName = 1; // e.g., "python_runner", "llm_orchestrator"
          string dockerImage = 2; // Specific Docker image to use for this pool
          int32 minInstances = 3; // Minimum desired running instances
          int32 maxInstances = 4; // Maximum allowed running instances (for scaling)
          ResourceLimits resourceLimits = 5; // CPU/Memory limits for containers <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
          repeated string volumeMounts = 6; // Volume mounts needed (e.g., for code, state access) <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
        }
        message ResourceLimits { string cpuLimit = 1; /*e.g., "0.5"*/ string memoryLimit = 2; /*e.g., "512M"*/ }
        message StateConfig { string type = 1; /* e.g., "git_yaml" */ map<string, string> params = 2; /* e.g., {"repoUrl": "...", "basePath": "state/"} */ }
        message ComponentRegistry { repeated ComponentDefinition components = 1; }
        message ComponentDefinition {
            string componentId = 1; // Unique ID for this logical component/handler/workflow
            HandlerType handlerType = 2; // LLM, JIT, WORKFLOW <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
            string targetPoolName = 3; // Which sandbox pool handles this <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
            map<string, string> taskDetails = 4; // Details specific to the handlerType <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
                                                 // e.g., { "script": "...", "function": "..." } for JIT
                                                 // e.g., { "prompt_template": "..." } for LLM
                                                 // e.g., { "workflowId": "..." } for WORKFLOW
            string expectedResultFormat = 5; // "generic" | "httpResponse" | "error" <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
            RouteMatcher routeMatcher = 6; // Optional: If triggered by HTTP requests
            map<string, google.protobuf.Value> configurationOverrides = 7; // Component-specific config
        }
        enum HandlerType { HANDLER_TYPE_UNSPECIFIED = 0; HANDLER_TYPE_LLM = 1; HANDLER_TYPE_JIT = 2; HANDLER_TYPE_WORKFLOW = 3; }
        message RouteMatcher { string pathPattern = 1; /* e.g., /api/users/:id */ repeated string methods = 2; /* e.g., ["GET", "POST"] */ }
        message SecurityConfig { repeated ApiKeyDefinition apiKeys = 1; repeated InterAppPermission interAppPermissions = 2; map<string, UserRoleDefinition> userRoles = 3;}
        message ApiKeyDefinition { string keyHash = 1; /* Hash of the key */ string description = 2; repeated string permissions = 3; /* Permissions associated */ bool enabled = 4;}
        message InterAppPermission { string allowedSourceAppId = 1; repeated string allowedEvents = 2; }
        message UserRoleDefinition { string roleName = 1; repeated string permissions = 2;}
        message OptimizationConfig {
            bool enabled = 1;
            repeated OptimizationRule rules = 2; // Global/App-level rules applied by Oracle <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
            // Could also include component-level overrides within ComponentDefinition
        }
        message OptimizationRule {
            string description = 1;
            MetricCondition condition = 2; // e.g., latency > 1s AND count > 10/min
            OptimizationAction action = 3; // e.g., TRIGGER_JIT
            map<string, google.protobuf.Value> actionParams = 4; // Params for the action
            bool preferLlmFlexibility = 5; // Hint for the Oracle <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
        }
        message MetricCondition { string expression = 1; /* e.g., "avg(latency_ms) > 1000 && count(requests) > 600" */ }
        enum OptimizationAction { ACTION_UNSPECIFIED = 0; ACTION_TRIGGER_JIT = 1; ACTION_RECOMMEND_JIT = 2; /* ... other actions ... */ }

        ```
    *   **Response:** `RegisterApplicationResponse`
        ```protobuf
        message RegisterApplicationResponse {
          string appId = 1; // Confirmed App ID
          bool success = 2;
          optional string error = 3; // Describes failure reason if success is false
        }
        ```

*   **`UpdateApplication`**
    *   **Purpose:** Applies partial updates to an existing application's definition (e.g., changing sandbox requirements, updating a component definition, modifying configuration or security rules). Typically triggered via the Admin Panel [1].
    *   **Request:** `UpdateApplicationRequest`
        ```protobuf
        message UpdateApplicationRequest {
          string appId = 1;
          // Uses field masks (`google.protobuf.FieldMask`) to specify which parts of the AppDefinition are being updated.
          google.protobuf.FieldMask update_mask = 2;
          AppDefinition updated_definition_fields = 3; // Contains only the fields specified in the mask
        }
        ```
    *   **Response:** `UpdateApplicationResponse`
        ```protobuf
        message UpdateApplicationResponse {
          bool success = 1;
          optional string error = 2;
        }
        ```

*   **`DeregisterApplication`**
    *   **Purpose:** Deactivates or completely removes an application from framework management. This should signal the `SandboxManager` to terminate associated sandboxes and potentially clean up state [1].
    *   **Request:** `DeregisterApplicationRequest`
        ```protobuf
        message DeregisterApplicationRequest {
          string appId = 1;
          bool deleteState = 2; // Flag to indicate if persistent state (e.g., Git repo) should also be removed. Defaults to false.
        }
        ```
    *   **Response:** `DeregisterApplicationResponse`
        ```protobuf
        message DeregisterApplicationResponse {
          bool success = 1;
          optional string error = 2;
        }
        ```

*   **`GetApplicationStatus`**
    *   **Purpose:** Retrieves the current runtime status of an application (e.g., Active, Inactive, Degraded, Error), potentially querying `SandboxManager` or health checks.
    *   **Request:** `GetApplicationStatusRequest`
        ```protobuf
        message GetApplicationStatusRequest {
          string appId = 1;
        }
        ```
    *   **Response:** `GetApplicationStatusResponse`
        ```protobuf
        message GetApplicationStatusResponse {
          string appId = 1;
          AppStatus status = 2;
          optional string details = 3; // e.g., Error message, number of running instances
        }
        enum AppStatus { APP_STATUS_UNSPECIFIED = 0; APP_STATUS_ACTIVE = 1; APP_STATUS_INITIALIZING = 2; APP_STATUS_INACTIVE = 3; APP_STATUS_DEGRADED = 4; APP_STATUS_ERROR = 5; }
        ```

*   **`ListActiveApplications`**
    *   **Purpose:** Returns IDs of all applications currently managed by the framework and considered active and running. Crucial for `SandboxManager` to know which applications require resources [1].
    *   **Request:** `ListActiveApplicationsRequest` (Empty)
    *   **Response:** `ListActiveApplicationsResponse`
        ```protobuf
        message ListActiveApplicationsResponse {
          repeated string appIds = 1;
        }
        ```

#### 3.1.3. Methods (Configuration & Requirements Retrieval)

These methods provide read access to the detailed configuration and requirements of specific applications, used heavily by other framework components.

*   **`GetApplicationDetails`**
    *   **Purpose:** Retrieves the complete, current `AppDefinition` structure for a specific application.
    *   **Request:** `GetApplicationDetailsRequest`
        ```protobuf
        message GetApplicationDetailsRequest {
          string appId = 1;
        }
        ```
    *   **Response:** `GetApplicationDetailsResponse`
        ```protobuf
        message GetApplicationDetailsResponse {
          AppDefinition definition = 1; // The full application definition object
        }
        ```

*   **`GetSandboxRequirements`**
    *   **Purpose:** Provides the specific sandbox pool configuration (`SandboxPoolConfig`) needed for an application. Primarily used by the `SandboxManager` to know what Docker images, sizes, and settings to use for provisioning [1].
    *   **Request:** `GetSandboxRequirementsRequest`
        ```protobuf
        message GetSandboxRequirementsRequest {
          string appId = 1;
        }
        ```
    *   **Response:** `GetSandboxRequirementsResponse`
        ```protobuf
        message GetSandboxRequirementsResponse {
          string appId = 1;
          SandboxPoolConfig requirements = 2; // Corresponds to AppDefinition.sandboxPools
        }
        ```

*   **`GetComponentDefinition`**
    *   **Purpose:** Retrieves the handling details for a specific component within an application, matched either by its unique `componentId` or by an incoming route (path + method). Primarily used by the `RequestRouter` to determine how to handle an incoming request/event [1].
    *   **Request:** `GetComponentDefinitionRequest`
        ```protobuf
        message GetComponentDefinitionRequest {
          string appId = 1;
          oneof identifier {
            string componentId = 2;   // Lookup by component ID directly
            RouteMatchInput routeInput = 3; // Lookup by matching HTTP route pattern
          }
        }
        message RouteMatchInput { string path = 1; /* Raw request path */ string method = 2; /* HTTP method */ }
        ```
    *   **Response:** `GetComponentDefinitionResponse`
        ```protobuf
        message GetComponentDefinitionResponse {
          bool found = 1; // Was a matching component definition found?
          optional ComponentDefinition definition = 2; // The definition if found
          optional map<string, string> extractedPathParameters = 3; // If lookup was by route, contains extracted params (e.g., {"id": "123"})
        }
        ```

*   **`GetAppConfigurationValue`**
    *   **Purpose:** Retrieves a specific configuration value associated with an application, potentially merging global, app-level, and component-level configurations. Useful for components needing specific settings (e.g., an LLM client needing an API base URL) and accessible to sandboxes via the `core.framework.getConfigValue` MCP tool [1].
    *   **Request:** `GetAppConfigurationValueRequest`
        ```protobuf
        message GetAppConfigurationValueRequest {
          string appId = 1;
          string key = 2; // Key to retrieve (e.g., "llm.provider", "externalServices.email.apiKey")
          optional string componentId = 3; // Optional context for component-specific overrides
        }
        ```
    *   **Response:** `GetAppConfigurationValueResponse`
        ```protobuf
        message GetAppConfigurationValueResponse {
          string key = 1;
          bool found = 2;
          optional google.protobuf.Value value = 3; // Standard proto type for arbitrary JSON-like value (string, number, bool, object, array)
        }
        ```

#### 3.1.4. Methods (Security: Validation & Permissions Retrieval)

These methods support the framework's security model, allowing validation of credentials and retrieval of permission sets.

*   **`ValidateApiKey`**
    *   **Purpose:** Checks if a provided API key is valid for any registered application and returns its associated application ID and permissions. Used by ingress/authentication layers [1].
    *   **Request:** `ValidateApiKeyRequest`
        ```protobuf
        message ValidateApiKeyRequest {
          string apiKey = 1; // The raw API key provided by the client
        }
        ```
    *   **Response:** `ValidateApiKeyResponse`
        ```protobuf
        message ValidateApiKeyResponse {
          bool isValid = 1;
          optional string appId = 2; // The Application ID the key belongs to, if valid
          repeated string permissions = 3; // List of permissions granted by this key, if valid
        }
        ```
    *   *Security Note:* Internally, this service MUST hash the input `apiKey` using a secure, one-way hashing algorithm (like Argon2 or bcrypt) with appropriate salts and compare it against stored hashes in the `SecurityConfig` for registered applications. Plaintext keys should never be stored [1].

*   **`GetApplicationPermissions`**
    *   **Purpose:** Retrieves the defined permission rules governing the application itself, such as which other applications are allowed to trigger it or which external services it can interact with. Potentially used by `RequestRouter` or MCP servers for authorization checks.
    *   **Request:** `GetApplicationPermissionsRequest`
        ```protobuf
        message GetApplicationPermissionsRequest {
          string appId = 1;
        }
        ```
    *   **Response:** `GetApplicationPermissionsResponse`
        ```protobuf
        message GetApplicationPermissionsResponse {
          // Structure mirrorring relevant parts SecurityConfig, e.g.,
          repeated InterAppPermission interAppPermissions = 1;
          // Could also include outbound permissions, etc.
        }
        ```

*   **`GetUserPermissionsForApp`**
    *   **Purpose:** Retrieves the specific permissions a given user has within the context of a specific application, based on their assigned roles. Used to populate the `context.userInfo.roles` or for fine-grained authorization checks.
    *   **Request:** `GetUserPermissionsForAppRequest`
        ```protobuf
        message GetUserPermissionsForAppRequest {
          string appId = 1;
          string userId = 2; // Identifier for the user
          // May need info about user's groups/external roles from Auth provider
        }
        ```
    *   **Response:** `GetUserPermissionsForAppResponse`
        ```protobuf
        message GetUserPermissionsForAppResponse {
          repeated string assignedRoles = 1; // Roles assigned to the user for this app
          repeated string calculatedPermissions = 2; // The effective permissions derived from the roles (based on UserRoleDefinition in SecurityConfig)
        }
        ```

#### 3.1.5. Core Data Structures

The core data structures like `AppDefinition`, `SandboxPoolConfig`, `ComponentDefinition`, `SecurityConfig`, etc., are defined within the method requests/responses above, providing a detailed schema for application representation within the framework.

### 3.2. `SandboxManager` Specification (Version 1.0)

#### 3.2.1. Purpose & Responsibilities

The `SandboxManager` is responsible for the practical management of the Docker container instances that serve as the Sandboxed Components for all active UHLP applications [1]. It translates the abstract requirements defined in the `ApplicationRegistry` into concrete Docker operations, ensuring the necessary execution environments are available, healthy, and scaled appropriately (within V1 limits) [1].

Its primary responsibilities are:
1.  Discovering application requirements from the `ApplicationRegistry` [1].
2.  Managing Docker resources (containers, images, networks, volumes) via the Docker API [1].
3.  Maintaining the configured number of running instances for each application's sandbox pools [1].
4.  Monitoring the health of sandbox instances and recycling unhealthy ones [1].
5.  Tracking the allocation state of instances (e.g., idle/busy).
6.  Providing an API for the `RequestRouter` to allocate available instances [1].

#### 3.2.2. Discovery (Via `ApplicationRegistry` API)

The `SandboxManager` does not read application state files directly [1]. It relies on the `ApplicationRegistryService` as its source of truth [1]. It periodically (e.g., every 10-30 seconds) performs the following:
1.  Calls `ApplicationRegistryService.ListActiveApplications()` to get the list of all currently active `appId`s [1].
2.  For each active `appId`, it calls `ApplicationRegistryService.GetSandboxRequirements()` to retrieve the `SandboxPoolConfig` detailing the required pools (images, sizes, resources, mounts) for that specific application [1].
3.  It compares this desired state with its internal registry of currently running containers and initiates actions (start, stop) to reconcile the differences.

#### 3.2.3. Docker Resource Management (via Docker Socket)

The `SandboxManager` requires direct access to the host's Docker daemon socket (typically `/var/run/docker.sock`) to perform its functions [1]. It uses a Docker client library (compatible with the API version) to:
*   **Pull Images:** Ensures the Docker images specified in `PoolDefinition.dockerImage` are available locally, pulling them if necessary.
*   **Create/Start Containers:** Uses the equivalent of `docker run`, configuring:
    *   The correct `dockerImage`.
    *   Resource constraints (`cpuLimit`, `memoryLimit` from `ResourceLimits`) [1].
    *   Necessary `volumeMounts` (e.g., mapping application state/code directories from the host or a shared volume into the container) [1].
    *   Network configuration (e.g., attaching to a specific Docker network for communication with the framework and MCP servers).
    *   Environment variables (potentially passing `appId`, `poolName`, or other context).
    *   Security options (e.g., running as a non-root user if the image supports it).
*   **Stop/Remove Containers:** Gracefully stops (`docker stop`) and removes (`docker rm`) containers when an application is deregistered, a pool is scaled down, or an instance needs recycling [1].
*   **Inspect/Monitor:** Uses `docker ps`, `docker inspect`, `docker stats` to get the status, network address, resource usage, and health of running containers [1].

#### 3.2.4. Pool Management (Per-Application Pools)

The `SandboxManager` manages resources on a per-application basis [1]. For each distinct `appId`, it ensures that the sandbox pools defined in its `SandboxPoolConfig` are maintained:
*   It aims to keep at least `minInstances` running and healthy for each defined pool [1].
*   It will automatically start new instances if the count drops below `minInstances` (e.g., due to crashes or scaling up from zero).
*   (Future V2+) If load increases (monitored via `MetricCollector` or allocation requests), it could proactively scale up the number of instances towards `maxInstances`. For V1, it might simply maintain `minInstances`.

#### 3.2.5. Health Monitoring & Recycling (Basic V0.1)

The V0.1 health monitoring is basic:
*   The `SandboxManager` uses the Docker API to check if containers are still in a `running` state [1].
*   If a container exits unexpectedly or becomes unresponsive (based on Docker API status), the `SandboxManager` will remove it [1].
*   It will then typically start a new instance to replace the failed one, ensuring the pool size stays at `minInstances` [1].
*   *Note:* V0.1 does not include sophisticated internal health checks (calling `/healthz` endpoints inside the sandbox) or complex recycling policies (e.g., restarting after N requests), although these could be added later.

#### 3.2.6. Instance Allocation API (`AllocateSandbox`/`ReleaseSandbox`)

The `SandboxManager` provides an internal API (likely simple method calls if co-located with Router, or gRPC if separate process) for the `RequestRouter` to obtain a network address for an available sandbox instance when needed [1].

*   **`AllocateSandbox(request: AllocateSandboxRequest) -> AllocateSandboxResponse`**
    *   **Purpose:** Called by `RequestRouter` to get an available instance from a specific pool for a given application.
    *   **Request:**
        ```protobuf
        message AllocateSandboxRequest {
          string appId = 1;
          string requiredPoolName = 2; // e.g., "python_runner", "llm_orchestrator"
          // optional string preferredInstanceId = 3; // For potential future sticky sessions
        }
        ```
    *   **Response:**
        ```protobuf
        message AllocateSandboxResponse {
          AllocationStatus status = 1; // ALLOCATED, NO_INSTANCE_AVAILABLE, POOL_NOT_FOUND
          optional string containerId = 2; // The Docker container ID allocated
          optional string networkAddress = 3; // The usable network address (e.g., "172.17.0.5:8080") for the /execute call
          optional string error = 4; // Reason if status is not ALLOCATED
        }
        enum AllocationStatus { ALLOCATION_STATUS_UNSPECIFIED = 0; ALLOCATION_STATUS_ALLOCATED = 1; ALLOCATION_STATUS_NO_INSTANCE_AVAILABLE = 2; ALLOCATION_STATUS_POOL_NOT_FOUND = 3;}
        ```
    *   **Implementation (V0.1):** Maintains an internal map of `appId -> poolName -> list_of_running_instances`. When `AllocateSandbox` is called, it finds the list for the given `appId` and `poolName`. It selects an instance using a simple strategy (e.g., round-robin over the list). If no instances are available (e.g., all busy if tracking state, or list is empty), it returns `NO_INSTANCE_AVAILABLE`. It returns the container's network address obtained via Docker inspection. *Tracking busy state might be deferred past V0.1, relying on sufficient `minInstances`.*

*   **`ReleaseSandbox(request: ReleaseSandboxRequest)` (Potentially deferred past V0.1)**
    *   **Purpose:** Called by `RequestRouter` after it finishes interacting with an allocated sandbox instance, allowing the `SandboxManager` to mark it as `idle` again (if tracking busy state).
    *   **Request:**
        ```protobuf
        message ReleaseSandboxRequest {
          string containerId = 1; // ID of the instance being released
        }
        ```
    *   *Note:* If V0.1 uses simple round-robin allocation without tracking busy state, this method might not be strictly necessary initially.

### 3.3. `StateManagerInterface` Internal API Specification (Version 1.0)

#### 3.3.1. Purpose & Transport (gRPC)

The `StateManagerInterface` provides a consistent, abstracted internal API for other Core Framework components (and the `CoreMCPServer`, acting on behalf of sandboxes) to interact with the state of UHLP applications [1]. It hides the underlying storage details, whether it's interacting with a Git repository containing YAML files for definition/configuration state or with a Redis instance for ephemeral runtime state [1]. It enforces necessary locking or concurrency control mechanisms appropriate for the underlying store [1].

**Transport Protocol:** Internal gRPC is preferred [1].

**Service Name:** `uhlp.framework.StateManagerService`

#### 3.3.2. State Scopes (Definition/Config vs. Runtime)

The API distinguishes between two primary types of state:
*   **Definition/Config State:** The versioned application definition, component registry, workflow YAMLs, prompt templates, etc., stored as files (primarily YAML) within a Git repository associated with the `appId` [1]. Accessed using file-path-based operations.
*   **Runtime State:** Ephemeral key-value data used for session management, temporary workflow variables, caching, locks, etc. Typically stored in Redis for performance [1]. Accessed using key-based operations.

All operations are implicitly or explicitly scoped to a specific `appId` provided by the caller.

#### 3.3.3. Definition State Methods (Git/YAML Operations)

These methods interact with the version-controlled file-based state. Paths are relative to the application's state root directory in Git.

*   **`GetDefinitionFileContent`**
    *   **Purpose:** Reads the content of a specific state file at a given revision (defaults to current).
    *   **Request/Response:** (As specified previously)
        *   `Request: { appId, filePath, revision? }`
        *   `Response: { found, content, revision, error? }`
    *   **Implementation:** Uses Git commands (`git show revision:filePath`) or a Git library to retrieve content.

*   **`ApplyDefinitionDiff`**
    *   **Purpose:** **Primary modification method.** Atomically applies a provided patch/diff to a file, ensuring it applies against the expected base revision (optimistic concurrency). Commits the change to Git [1].
    *   **Request/Response:** (As specified previously)
        *   `Request: { appId, filePath, diffContent, expectedBaseRevision, commitMessage, author? }`
        *   `Response: { success, resultingRevision, error? }`
    *   **Implementation:** Requires careful implementation: Acquire a lock (e.g., file-based lock, or Redis lock) for the `appId` + `filePath`; clone/pull the repo if necessary; check out `expectedBaseRevision`; attempt to apply the `diffContent` using a patch utility; if successful, commit the change with message/author; push the change (if remote repo); release lock. Handle merge conflicts/patch failures gracefully.

*   **`SetDefinitionFileContent`**
    *   **Purpose:** Overwrites or creates a state file. Should be used cautiously; `ApplyDefinitionDiff` is preferred for modifications [1].
    *   **Request/Response:** (As specified previously)
        *   `Request: { appId, filePath, content, commitMessage, author? }`
        *   `Response: { success, resultingRevision, error? }`
    *   **Implementation:** Similar locking/commit/push flow as `ApplyDefinitionDiff`, but overwrites the file content directly.

*   **`DeleteDefinitionFile`**
    *   **Purpose:** Deletes a state file within the Git repository [1].
    *   **Request/Response:** (As specified previously)
        *   `Request: { appId, filePath, commitMessage, author? }`
        *   `Response: { success, resultingRevision, error? }`
    *   **Implementation:** Similar locking/commit/push flow, using `git rm`.

*   **`ListDefinitionDirectory`**
    *   **Purpose:** Lists files and subdirectories within the state repository [1].
    *   **Request/Response:** (As specified previously)
        *   `Request: { appId, directoryPath, recursive?, revision? }`
        *   `Response: { entries: [{path, type}], revision, error? }`
    *   **Implementation:** Uses Git commands (`git ls-tree`) or library equivalents.

#### 3.3.4. Runtime State Methods (Redis Operations)

These methods interact with the ephemeral key-value store (assumed Redis). Keys are implicitly namespaced by `appId`.

*   **`SetRuntimeValue`**
    *   **Purpose:** Sets or updates a key-value pair, optionally with a TTL [1].
    *   **Request/Response:** (As specified previously)
        *   `Request: { appId, key, value: google.protobuf.Value, ttlSeconds? }`
        *   `Response: { success, error? }`
    *   **Implementation:** Connects to Redis, uses `SET` command (with `EX` option if `ttlSeconds` is provided). Value serialization (e.g., JSON for `google.protobuf.Value`) needs to be handled. Keys should be prefixed internally (e.g., `uhlp:runtime:<appId>:<key>`).

*   **`GetRuntimeValue`**
    *   **Purpose:** Retrieves a value by key [1].
    *   **Request/Response:** (As specified previously)
        *   `Request: { appId, key }`
        *   `Response: { found, value?: google.protobuf.Value, error? }`
    *   **Implementation:** Uses Redis `GET` command. Handles deserialization from stored format (e.g., JSON) back to `google.protobuf.Value`.

*   **`DeleteRuntimeValue`**
    *   **Purpose:** Deletes a key [1].
    *   **Request/Response:** (As specified previously)
        *   `Request: { appId, key }`
        *   `Response: { success, error? }`
    *   **Implementation:** Uses Redis `DEL` command.

*   **`IncrementRuntimeValue` (Optional)**
    *   **Purpose:** Atomic increment for counters.
    *   **Implementation:** Uses Redis `INCRBY` command.

### 3.4. `RequestRouter` Specification (Version 1.1)

#### 3.4.1. Purpose & Hosting

The `RequestRouter` is the central traffic director within the Core Framework [1]. It receives incoming processed events, determines the appropriate target (a specific component or workflow within a specific application), allocates a suitable Sandbox instance via the `SandboxManager`, constructs the detailed execution request, dispatches it to the sandbox, and handles the response to formulate the final outcome [1].

**Hosting:** Runs as a core module/process within the Core Framework deployment. It needs network connectivity to the `ApplicationRegistry`, `SandboxManager`, `MetricCollector`, and the internal network addresses of the Sandbox containers.

#### 3.4.2. Input & Core Logic Flow

**(As specified previously)** Receives processed event data (`appId`, `source`, `sourceDetails`, `traceId`) and executes the core logic flow: Identify Target -> Allocate Sandbox -> Construct `/execute` Request -> Dispatch -> Handle Response -> Release Sandbox (if needed) [1].

#### 3.4.3. Component/Workflow Identification (Via `ApplicationRegistry`)

Uses `ApplicationRegistryService.GetComponentDefinition` with `appId` and `sourceDetails` to find the `ComponentDefinition`. Critically examines `handlerType` to distinguish between direct `JIT`/`LLM` calls and `WORKFLOW` initiation [1]. Extracts `targetPoolName`, `taskDetails` (script/function, prompt, or `workflowId`), and `expectedResultFormat` [1].

#### 3.4.4. Sandbox Allocation (Via `SandboxManager`)

Uses `SandboxManager.AllocateSandbox` with `appId` and the determined `targetPoolName` to get the `networkAddress` of an available instance [1]. Handles allocation failures (e.g., return 503).

#### 3.4.5. `/execute` Request Construction (Handling Workflow vs. Direct Call)

Constructs the detailed JSON body for the `POST /execute` call as defined in **Section 2.4**. Includes `requestData` based on the source, and `context` including `appId`, `componentId`, `mcp_endpoint`, state/auth/config info. **Specifically adds `context.workflowInfo { workflowId }` if the target `handlerType` is `WORKFLOW`** to instruct the orchestrator sandbox [1].

#### 3.4.6. Sandbox Response Handling & Final Response Generation

Receives the response from the sandbox `/execute` call. Handles HTTP errors. On success (200 OK), parses the body, forwards `metrics` to `MetricCollector`, and processes the `data` based on `resultType` (`httpResponse`, `generic`, `error`) to formulate the final response appropriate for the original `source` [1].

### 3.5. `MetricCollector` Specification (Version 1.0)

#### 3.5.1. Purpose & Hosting

The `MetricCollector` aggregates and provides standardized access to operational metrics from framework components and sandboxes [2]. It decouples metric producers from consumers (like monitoring dashboards) [4].

**Hosting:** Can run integrated within the Core Framework (dev mode) or as a separate container/pool (prod mode) [4]. Needs to accept internal API calls and expose an HTTP endpoint.

#### 3.5.2. Input Interface (Push API - OTLP Inspired)

Components (like `RequestRouter`, `SandboxManager`, potentially MCP servers) push metrics via an internal API (gRPC `RecordMetrics` or `POST /v1/metrics`) using a structure inspired by the OpenTelemetry Metrics Data Model (Gauges, Sums, Histograms with mandatory attributes) [1, 3].

#### 3.5.3. Key Attributes/Labels (`appId`, `componentId`, etc.)

Requires standard attributes (`appId`, `componentId`, `sandboxId`, `handlerType`, `poolName`, etc.) on all received metric points for effective filtering and aggregation [1].

#### 3.5.4. Output Interface (Prometheus Exposition Format via `GET /metrics`)

Exposes collected metrics via an HTTP `GET /metrics` endpoint adhering to the Prometheus exposition format [4]. Translates internal OTLP-like representation to Prometheus text format on demand [4].

#### 3.5.5. Extensibility (Handling Custom Metrics)

Automatically handles custom application metrics (e.g., `app.custom.*`) as long as they are pushed with consistent names and mandatory attributes. No special configuration needed on the collector itself for new custom metric names [2].

### 3.6. `OptimizationOracle` Specification (V0.2 - Enhanced Control)

#### 3.6.1. Purpose & Hosting

The `OptimizationOracle` analyzes runtime metrics to identify opportunities for JIT compilation, balancing performance/cost gains against potential loss of flexibility [1]. It orchestrates the process of generating JIT code and updating the application's state to use it [1].

**Hosting:** Runs as a background processing module/service within the Core Framework.

#### 3.6.2. Data Acquisition (Via `MetricCollector`)

Periodically fetches or subscribes to aggregated metrics from the `MetricCollector` (latency, token counts, call frequency, error rates) grouped by `appId` and `componentId` [1].

#### 3.6.3. Decision Trigger (Rule-Based via Admin Panel Config: Global/App/Component)

Reads optimization rules and flags (`preferLlmFlexibility`) from the application's definition (via `ApplicationRegistryService`) configured at global, per-app, or per-component levels [1]. Evaluates metrics against these rules. May trigger automatically or generate recommendations based on configuration [1].

#### 3.6.4. Manual Trigger Support

Responds to explicit JIT trigger requests initiated via an internal API (called potentially from the Admin Panel via `ApplicationRegistry`) [1].

#### 3.6.5. JIT Process Initiation (Spec Generation, Coder LLM Invocation, Artifact Storage via `StateManager`)

When triggered, formulates a spec for the target component, invokes a "Coder LLM" (via `core.llm.generate` MCP call) requesting code and tests, and stores the resulting artifacts (e.g., `_jit_code/.../handler.py`) into the application's versioned state using `StateManagerInterface.SetDefinitionFileContent` [1].

#### 3.6.6. Triggering State Update (No HotReloadManager needed for V0.1)

After successfully storing JIT artifacts, calls `StateManagerInterface.ApplyDefinitionDiff` to update the application's `ComponentRegistry` state, changing the `handlerType` to `jit` and setting the `taskDetails` to point to the new script path. This directs future requests handled by the `RequestRouter` to the JIT execution path [1].