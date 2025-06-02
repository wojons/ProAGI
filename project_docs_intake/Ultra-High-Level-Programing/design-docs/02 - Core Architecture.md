## 2. Core Architecture (Reference: UHLP Document Section II)

This section details the fundamental architectural components of the UHLP framework and how they interact. The architecture is designed around a stable core foundation that orchestrates dynamic, often AI-driven, components running in isolated environments.

### 2.1. Immutable Core Framework Overview

The **Immutable Core Framework** serves as the stable, foundational layer of the UHLP runtime environment [1]. Analogous to an operating system or a language runtime (like the JVM or Python interpreter), its primary role is to provide the necessary scaffolding, execution guarantees, monitoring capabilities, validation mechanisms, and core APIs for UHLP applications [1].

It is considered "immutable" in the sense that its own code is deployed and updated through traditional software development practices, remaining stable during the dynamic execution of the UHLP applications it hosts. Its key responsibilities include, but are not limited to:
*   Ingesting incoming requests from various sources (HTTP, internal triggers, callbacks, scheduled jobs) [1].
*   Routing these requests to the appropriate Sandboxed Component based on the application's defined state [1].
*   Managing the entire lifecycle of Sandbox instances (provisioning, monitoring, scaling, termination) via the `SandboxManager` [1].
*   Providing access to and managing the application's state (both definition/config state in Git/YAML and runtime state in Redis) via the `StateManagerInterface` [1].
*   Collecting and exposing operational metrics via the `MetricCollector` [1].
*   Hosting the `CoreMCPServer` and potentially coordinating routing to other MCP servers, providing sandboxes with controlled access to tools and resources [1].
*   Validating inputs and potentially outputs (e.g., LLM response validation against schemas) [1].
*   Orchestrating the JIT optimization process via the `OptimizationOracle` [1].
*   Serving the dynamically generated user interface components [1].
*   Enforcing security policies and permissions [1].

The Core Framework itself is composed of several internal modules (like `ApplicationRegistry`, `RequestRouter`, `SandboxManager`, `StateManagerInterface`, `MetricCollector`, `OptimizationOracle`) working together to provide this stable operational environment [1].

### 2.2. Sandboxed Components Overview (Docker Containers)

The dynamic logic of a UHLP application—whether it's direct LLM interpretation, JIT-compiled code execution, or workflow orchestration—runs within **Sandboxed Components** [1]. For V0.1, these sandboxes are implemented as **Docker Containers**, managed by the `SandboxManager` [1].

#### 2.2.1. Sandbox Types (JIT Runner, LLM Orchestrator/Runner)

Different types of sandboxes exist, typically grouped into pools dedicated to specific applications [1]. Common types include:

*   **JIT Runner:** Optimized for executing JIT-generated code in a specific language (e.g., a Python JIT runner, a Node.js JIT runner). These containers include the necessary language runtime and potentially common libraries pre-installed. They receive `/execute` calls containing task details like the script path and function name [1].
*   **LLM Orchestrator/Runner:** Specialized in interacting with LLMs (via MCP calls) and potentially capable of orchestrating multi-step workflows by interpreting the Workflow YAML definition [1, 4]. These receive `/execute` calls indicating a workflow needs to start or an LLM prompt needs processing [1].

The specific types and configurations of sandboxes required by an application are defined in its `AppDefinition` within the state and managed by the `ApplicationRegistry` and `SandboxManager` [1].

#### 2.2.2. Execution Model (V0.1: Interpreter Mode for JIT)

For the initial version (V0.1), JIT code execution within JIT Runner sandboxes primarily uses an **"Interpreter Mode"** [1]. When the sandbox container receives an `/execute` request specifying a JIT task (script + function), the lightweight HTTP server inside the container invokes the appropriate language interpreter (e.g., `python`) directly on the target script file. This script file is made available within the container via shared Docker volume mounts defined by the `SandboxManager` based on the application's state [1]. Input data is passed (e.g., via stdin, arguments, temp files), and output is captured. This model simplifies V0.1 by avoiding the need for complex hot-reloading mechanisms within the sandbox process itself, as each execution potentially uses the latest version of the script file present on the mounted volume [1].

#### 2.2.3. Isolation Purpose

The primary purpose of using Docker containers for sandboxing in UHLP V0.1 is **dependency management and environment consistency**, similar to using a Python `virtualenv` [1]. It ensures that the specific language versions, libraries, and system dependencies required by an application's JIT code or LLM interactions are isolated from the host system and other UHLP applications [1]. While Docker provides process isolation, it is not initially intended as a hardened security boundary against intentionally malicious code execution within the sandbox (though security best practices like running as non-root users and resource limiting are employed) [1]; stronger isolation (like Firecracker microVMs [4]) could be considered in future versions if security requirements demand it.

### 2.3. Interaction Model (Request Flow)

A typical request flows through the UHLP system as follows:

1.  **Ingestion:** An incoming request (e.g., User HTTP request, internal trigger, webhook callback) arrives at the Core Framework's entry point (e.g., load balancer, ingress controller) [1].
2.  **Initial Handling:** An initial component (e.g., `RequestIngestor`) performs basic validation, identifies the target `appId` (e.g., from hostname or API key validated via `ApplicationRegistry`), extracts source details, and forwards the processed event information to the `RequestRouter` [1].
3.  **Routing Decision:** The `RequestRouter` consults the `ApplicationRegistry` using the `appId` and event details (e.g., path, method) to find the corresponding `ComponentDefinition` in the application's state [1]. This definition indicates the handler type (`LLM`, `JIT`, `WORKFLOW`), the required sandbox pool (`targetPoolName`), and specific task details (prompt, script/function, `workflowId`) [1].
4.  **Sandbox Allocation:** The `RequestRouter` requests an available sandbox instance from the appropriate pool (`targetPoolName` for the specified `appId`) by calling the `SandboxManager.AllocateSandbox` API [1].
5.  **Context Assembly:** The `RequestRouter` gathers necessary context information, including user details (from Auth component), session ID, relevant configuration values (from `ApplicationRegistry`), the `mcp_endpoint` URL, and the specific `taskDetails` or `workflowInfo` [1].
6.  **Sandbox Execution Call:** The `RequestRouter` constructs the JSON payload for the `POST /execute` request (containing `requestData` and `context`) and sends it to the allocated Sandbox container's internal HTTP server address (provided by `SandboxManager`) [1].
7.  **Sandbox Processing:** The Sandbox container receives the `/execute` request. Its internal server/runner:
    *   Parses the request.
    *   If it's a JIT task (Interpreter Mode), it invokes the specified script/function using the language interpreter, passing inputs from `requestData` and `context` [1].
    *   If it's an LLM task, it loads the prompt template (via `core.state.getDefinitionFileContent` MCP call), renders it using Jinja2 and context variables, and calls the `core.llm.generate` MCP tool [1].
    *   If it's a Workflow task, it loads the specified Workflow YAML (via `core.state.getDefinitionFileContent` MCP call) and starts executing the steps defined within, potentially making further JIT, LLM, or MCP calls as required by the workflow definition [1, 4].
    *   During processing, the sandbox can interact with state (`core.state.*`), configuration (`core.framework.getConfigValue`), tools (`core.linux.executeCommand`, `community.*`, `app.*`), etc., via calls to its designated Application-Specific MCP Server (`mcp_endpoint`) [1].
8.  **Sandbox Response:** The Sandbox completes its processing (or a workflow step) and constructs a response JSON object, including `resultType`, `data` (the outcome), and optional `metrics` [1]. It sends this back as the HTTP 200 OK response to the `/execute` call from the `RequestRouter`.
9.  **Response Handling:** The `RequestRouter` receives the response from the Sandbox [1].
    *   It forwards the `metrics` to the `MetricCollector` [1].
    *   It interprets the `resultType` and `data` based on the component's `expectedResultFormat` and the original request source [1].
    *   If the original source was HTTP and `resultType` is `httpResponse`, it uses the details (`statusCode`, `headers`, `body`) from the `data` field [1].
    *   If the original source was HTTP and `resultType` is `generic` or `error`, it formats an appropriate final HTTP response (e.g., 200 OK with generic data as JSON body, or 4xx/5xx with error details) [1].
    *   If the source was internal, it might pass the `data` along or handle completion/errors differently.
10. **Final Response:** The `RequestRouter` (or a downstream component) sends the final formatted response back to the original requester [1].
11. **Sandbox Release:** (If explicit release is used) The `RequestRouter` notifies the `SandboxManager` that the instance is free (`ReleaseSandbox`) [1].

### 2.4. Core Framework -> Sandbox API Specification (Version 1.0)

*(This subsection includes the full specification generated previously)*

**Endpoint:** `POST /execute` (Internal API within the Sandbox container)

**Purpose:** Provides the main mechanism for the Core Framework to invoke processing logic (LLM interaction, JIT code execution, workflow orchestration) within a dedicated sandbox container [1].

**Transport Protocol:** HTTP/1.1 (Simpler initial target, upgradeable to HTTP/2 or gRPC later if needed) [1].

**Hosting:** Each Sandbox container runs a lightweight HTTP server (e.g., based on Python's `http.server`, FastAPI, Node's `http` module, etc.) listening on a designated internal port [1]. The Core Framework (`RequestRouter` + `SandboxManager`) resolves the container's internal IP/hostname and port [1].

**Request:**

*   **Headers:**
    *   `Content-Type: application/json` (Required)
    *   `Accept: application/json` (Required)
    *   `X-Request-ID: <uuid>` (Required - Unique ID generated by the Framework for tracing this specific invocation)
    *   `X-Trace-ID: <uuid>` (Optional - Trace ID spanning the entire end-to-end user request or workflow)
*   **Body:** JSON payload conforming to the following structure:

```json
{
  "requestId": "string", // Matches X-Request-ID header, for application-level tracking
  "requestData": { // Details of the event triggering this execution <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
    "source": "http" | "trigger" | "callback" | "queue" | "cron" | "internal", // Origin Type <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
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
    "callbackDetails": { // Present if source == 'callback'
       "callbackUrl": "string", // The URL the callback was received on
       "headers": {}, // Headers from the callback source
        "body": "string",
        "bodyEncoding": "utf8" | "base64"
    },
     "queueDetails": { // Present if source == 'queue'
       "queueName": "string",
       "messageId": "string",
       "payload": {} // JSON object payload from the queue message
    },
     "cronDetails": { // Present if source == 'cron'
       "jobId": "string",
       "scheduledTime": "string" // ISO 8601 timestamp
    }
    // Add other details objects as needed for 'internal', etc.
  },
  "context": { // Background information provided by the Framework <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
    "appId": "string", // Unique ID of the UHLP application this request belongs to <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
    "componentId": "string", // ID of the component/workflow being invoked (from state) <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
    "workflowInfo": { // Optional: Added if handlerType is WORKFLOW
        "workflowId": "string",
        "startAt": "string" // Optional starting step ID
    },
    "mcp_endpoint": "string", // URL for the App-Specific MCP Server the sandbox should use <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
    "stateConfig": { // Info about how the sandbox should access its state
        "type": "mcp_tool", // Assume state access is primarily via MCP tools initially
        "readTool": "core.state.getDefinitionFileContent",
        "writeTool": "core.state.applyStateDiff" // Tools provided by Core MCP <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
        // Could potentially support direct volume mounts later
    },
    "userInfo": { // Optional: Present if user context is available/authenticated <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
      "id": "string",
      "roles": ["string"],
      "isAuthenticated": true,
      "claims": {} // Optional: custom claims/attributes
    },
    "sessionId": "string", // Optional: Identifier for framework-managed session state <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
    "configuration": { // Select app-specific config values injected by Framework <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
        /* e.g., "externalApiUrl": "https://partner.com/api" */
    },
    "applicationInfo": { // General info about the running app <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
        "deploymentMode": "production" | "development" | "staging"
    }
    // Avoid passing sensitive Framework internals directly; use MCP for access <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
  }
}
```
**Response:**

- **Success Status Codes (HTTP Layer):**
    - `200 OK`: Sandbox received the request, processed it (successfully _or_ with an _application-level_ error defined in the body), and the response body contains the outcome.
- **Failure Status Codes (HTTP Layer):**
    - `400 Bad Request`: The request body JSON was malformed or contained invalid structure according to this spec.
    - `429 Too Many Requests`: (Optional) Sandbox is overloaded and cannot accept the request currently.
    - `500 Internal Server Error`: The sandbox encountered an _unhandled internal exception_ during execution (e.g., coding error in JIT script, internal crash).
    - `503 Service Unavailable`: The sandbox is temporarily unable to process requests (e.g., cannot connect to essential backend like MCP).
- **Headers:**
    - `Content-Type: application/json` (Required on success/application error)
    - `X-Request-ID: <uuid>` (Required - Echoing the request ID)
- **Body (on `200 OK`):** JSON payload conforming to the following structure:
```json
{
  "requestId": "string", // Matches request ID
  "resultType": "generic" | "httpResponse" | "error" | "workflowStep", // Type of result <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
  "data": {
      // --- Structure depends on resultType --- <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />

      // Type: "generic" - Raw data output, framework decides final formatting
      // Example: { "processedItems": 3, "results": [ ... ] }

      // Type: "httpResponse" - Defines the exact HTTP response for the framework to proxy
      // Example:
      // {
      //   "statusCode": 201,
      //   "headers": { "Content-Type": "application/json", "Location": "/api/items/456" },
      //   "body": "string", // Base64 encoded for binary, plain string otherwise
      //   "bodyEncoding": "utf8" | "base64"
      // }

      // Type: "error" - Application-level error identified by sandbox logic <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
      // Example:
      // {
      //   "code": "INSUFFICIENT_FUNDS",
      //   "message": "User does not have enough balance.",
      //   "details": { "currentBalance": 10.50 }
      // }

      // Type: "workflowStep" - Intermediate result from a workflow step execution (if orchestrated by sandbox)
      // Example:
      // {
      //    "workflowId": "user-reg-flow",
      //    "stepId": "validate-email",
      //    "status": "completed" | "failed",
      //    "output": { /* Data produced by this step */ },
      //    "error": { /* Optional error details if status is failed */ }
      // }
  },
  "metrics": { // Optional: Performance metrics from the Sandbox <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
     "execution_time_ms": 123,
     "mcp_calls": [
       { "tool": "core.state.getFileContent", "count": 2, "total_duration_ms": 15 },
       { "tool": "llm.openai.generate", "count": 1, "total_duration_ms": 95, "token_usage": { "prompt": 300, "completion": 150 } }
     ],
     // Other relevant sandbox-internal metrics
  }
}
```
**Body (on HTTP `4xx`/`5xx` Errors):** Optional JSON body providing error details from the sandbox's HTTP server itself.
```json
{ "error": "string", "details": "string" }
```