Okay, here is the comprehensive UHLP Framework Design Specification document, assembling all the sections (1 through 11), Glossary, and Appendixes based on our detailed discussions and specifications.

```markdown
# UHLP (Ultra High Level Programming) Framework Design Specification (V0.1)

## Table of Contents

1.  [Concept Overview](#1-concept-overview-reference-uhlp-document-section-i)
    1.1. [Core Idea: LLM as Runtime](#11-core-idea-llm-as-runtime)
    1.2. [Abstraction Layer](#12-abstraction-layer)
    1.3. [User Experience Analogy (Roblox-like)](#13-user-experience-analogy-roblox-like)
    1.4. [JIT / Adaptive Nature (Predictive, Reactive, Optimizing)](#14-jit--adaptive-nature-predictive-reactive-optimizing)
2.  [Core Architecture](#2-core-architecture-reference-uhlp-document-section-ii)
    2.1. [Immutable Core Framework Overview](#21-immutable-core-framework-overview)
    2.2. [Sandboxed Components Overview (Docker Containers)](#22-sandboxed-components-overview-docker-containers)
        2.2.1. [Sandbox Types (JIT Runner, LLM Orchestrator/Runner)](#221-sandbox-types-jit-runner-llm-orchestratorrunner)
        2.2.2. [Execution Model (V0.1: Interpreter Mode for JIT)](#222-execution-model-v01-interpreter-mode-for-jit)
        2.2.3. [Isolation Purpose](#223-isolation-purpose)
    2.3. [Interaction Model (Request Flow)](#23-interaction-model-request-flow)
    2.4. [Core Framework -> Sandbox API Specification (Version 1.0)](#24-core-framework---sandbox-api-specification-version-10)
3.  [Core Framework Internal Components & APIs](#3-core-framework-internal-components--apis)
    3.1. [`ApplicationRegistry` Internal API Specification (Version 1.0)](#31-applicationregistry-internal-api-specification-version-10)
        3.1.1. [Purpose & Transport (gRPC)](#311-purpose--transport-grpc)
        3.1.2. [Methods (Application Lifecycle & Management)](#312-methods-application-lifecycle--management)
        3.1.3. [Methods (Configuration & Requirements Retrieval)](#313-methods-configuration--requirements-retrieval)
        3.1.4. [Methods (Security: Validation & Permissions Retrieval)](#314-methods-security-validation--permissions-retrieval)
        3.1.5. [Core Data Structures](#315-core-data-structures)
    3.2. [`SandboxManager` Specification (Version 1.0)](#32-sandboxmanager-specification-version-10)
        3.2.1. [Purpose & Responsibilities](#321-purpose--responsibilities)
        3.2.2. [Discovery (Via `ApplicationRegistry` API)](#322-discovery-via-applicationregistry-api)
        3.2.3. [Docker Resource Management (via Docker Socket)](#323-docker-resource-management-via-docker-socket)
        3.2.4. [Pool Management (Per-Application Pools)](#324-pool-management-per-application-pools)
        3.2.5. [Health Monitoring & Recycling (Basic V0.1)](#325-health-monitoring--recycling-basic-v01)
        3.2.6. [Instance Allocation API (`AllocateSandbox`/`ReleaseSandbox`)](#326-instance-allocation-api-allocatesandboxreleasesandbox)
    3.3. [`StateManagerInterface` Internal API Specification (Version 1.0)](#33-statemanagerinterface-internal-api-specification-version-10)
        3.3.1. [Purpose & Transport (gRPC)](#331-purpose--transport-grpc)
        3.3.2. [State Scopes (Definition/Config vs. Runtime)](#332-state-scopes-definitionconfig-vs-runtime)
        3.3.3. [Definition State Methods (Git/YAML Operations)](#333-definition-state-methods-gityaml-operations)
        3.3.4. [Runtime State Methods (Redis Operations)](#334-runtime-state-methods-redis-operations)
    3.4. [`RequestRouter` Specification (Version 1.1)](#34-requestrouter-specification-version-11)
        3.4.1. [Purpose & Hosting](#341-purpose--hosting)
        3.4.2. [Input & Core Logic Flow](#342-input--core-logic-flow)
        3.4.3. [Component/Workflow Identification (Via `ApplicationRegistry`)](#343-componentworkflow-identification-via-applicationregistry)
        3.4.4. [Sandbox Allocation (Via `SandboxManager`)](#344-sandbox-allocation-via-sandboxmanager)
        3.4.5. [`/execute` Request Construction (Handling Workflow vs. Direct Call)](#345-execute-request-construction-handling-workflow-vs-direct-call)
        3.4.6. [Sandbox Response Handling & Final Response Generation](#346-sandbox-response-handling--final-response-generation)
    3.5. [`MetricCollector` Specification (Version 1.0)](#35-metriccollector-specification-version-10)
        3.5.1. [Purpose & Hosting](#351-purpose--hosting)
        3.5.2. [Input Interface (Push API - OTLP Inspired)](#352-input-interface-push-api---otlp-inspired)
        3.5.3. [Key Attributes/Labels (`appId`, `componentId`, etc.)](#353-key-attributeslabels-appid-componentid-etc)
        3.5.4. [Output Interface (Prometheus Exposition Format via `GET /metrics`)](#354-output-interface-prometheus-exposition-format-via-get-metrics)
        3.5.5. [Extensibility (Handling Custom Metrics)](#355-extensibility-handling-custom-metrics)
    3.6. [`OptimizationOracle` Specification (V0.2 - Enhanced Control)](#36-optimizationoracle-specification-v02---enhanced-control)
        3.6.1. [Purpose & Hosting](#361-purpose--hosting)
        3.6.2. [Data Acquisition (Via `MetricCollector`)](#362-data-acquisition-via-metriccollector)
        3.6.3. [Decision Trigger (Rule-Based via Admin Panel Config: Global/App/Component)](#363-decision-trigger-rule-based-via-admin-panel-config-globalappcomponent)
        3.6.4. [Manual Trigger Support](#364-manual-trigger-support)
        3.6.5. [JIT Process Initiation (Spec Generation, Coder LLM Invocation, Artifact Storage via `StateManager`)](#365-jit-process-initiation-spec-generation-coder-llm-invocation-artifact-storage-via-statemanager)
        3.6.6. [Triggering State Update (No HotReloadManager needed for V0.1)](#366-triggering-state-update-no-hotreloadmanager-needed-for-v01)
4.  [State Management Details](#4-state-management-details-reference-uhlp-document-section-iii)
    4.1. [Conceptual Content](#41-conceptual-content)
    4.2. [Storage Mechanisms](#42-storage-mechanisms)
        4.2.1. [Definition/Config: Git + YAML Files (Primary Source of Truth)](#421-definitionconfig-git--yaml-files-primary-source-of-truth)
        4.2.2. [Runtime Ephemeral State: Redis](#422-runtime-ephemeral-state-redis)
        4.2.3. [Application Domain Data: External Databases (via MCP)](#423-application-domain-data-external-databases-via-mcp)
    4.3. [Access API (Provided by `StateManagerInterface`)](#43-access-api-provided-by-statemanagerinterface)
5.  [Model Context Protocol (MCP)](#5-model-context-protocol-mcp-reference-uhlp-document-section-iv)
    5.1. [Role & Purpose](#51-role--purpose)
    5.2. [Multi-Server Architecture (Core, App-Specific, Community)](#52-multi-server-architecture-core-app-specific-community)
    5.3. [Scoping (Core=Shared, App/Community=Per-Application)](#53-scoping-coreshared-appcommunityper-application)
    5.4. [`CoreMCPServer` Specification (Summary)](#54-coremcpserver-specification-summary---see-section-35-for-full-details)
    5.5. [Non-Core Routing Example](#55-non-core-routing-example)
    5.6. [Modular Design](#56-modular-design)
6.  [Workflow Definition](#6-workflow-definition)
    6.1. [Workflow YAML Structure Specification (Version 1.0)](#61-workflow-yaml-structure-specification-version-10)
        6.1.1. [Purpose & File Location](#611-purpose--file-location)
        6.1.2. [Top-Level Properties (`workflowId`, `trigger`, `startAt`, `steps`)](#612-top-level-properties-workflowid-trigger-startat-steps)
        6.1.3. [Step Definition (`stepId`, `type`, `target`, `inputMapping`, `transitions`)](#613-step-definition-stepid-type-target-inputmapping-transitions)
        6.1.4. [Step Types (`jit`, `llm`, `mcp`, `control`)](#614-step-types-jit-llm-mcp-control)
        6.1.5. [Expression Syntax (V1 - Simple JSONPath-like / Dot Notation)](#615-expression-syntax-v1---simple-jsonpath-like--dot-notation)
        6.1.6. [Transitions & Flow Control (`onSuccess`, `onFailure`, `condition`, `end`)](#616-transitions--flow-control-onsuccess-onfailure-condition-end)
    6.2. [Execution Model](#62-execution-model)
    6.3. [Enhancements Inspired by n8n (V2+ Considerations)](#63-enhancements-inspired-by-n8n-v2-considerations)
7.  [Dynamic Execution & Optimization](#7-dynamic-execution--optimization-reference-uhlp-document-section-v)
    7.1. [Runtime Decision Making (Handled by `OptimizationOracle`)](#71-runtime-decision-making-handled-by-optimizationoracle)
    7.2. [Execution Paths (LLM vs. JIT)](#72-execution-paths-llm-vs-jit)
    7.3. [JIT Code Generation Workflow (Detailed within `OptimizationOracle`)](#73-jit-code-generation-workflow-detailed-within-optimizationoracle)
    7.4. [Multi-Layer Caching (Concept - Not Specified in Detail for V1)](#74-multi-layer-caching-concept---not-specified-in-detail-for-v1)
8.  [Prompt Template Format](#8-prompt-template-format)
    8.1. [LLM Prompt Template Format Specification (Version 1.0)](#81-llm-prompt-template-format-specification-version-10)
        8.1.1. [Purpose & File Format (YAML)](#811-purpose--file-format-yaml)
        8.1.2. [Structure (Metadata + `template`)](#812-structure-metadata--template)
        8.1.3. [Templating Engine (Jinja2)](#813-templating-engine-jinja2)
        8.1.4. [Output Specification (`outputFormat`, `outputSchema`)](#814-output-specification-outputformat-outputschema)
        8.1.5. [Processing Flow Summary](#815-processing-flow-summary)
9.  [UI & Application Lifecycle](#9-ui--application-lifecycle-reference-uhlp-document-section-vi--vii)
    9.1. [UI Generation](#91-ui-generation)
    9.2. [Bootstrap Process (Application Creation)](#92-bootstrap-process-application-creation)
    9.3. [Deployment & Access](#93-deployment--access)
    9.4. [Admin Panel Requirements (V1 Sketch)](#94-admin-panel-requirements-v1-sketch)
10. [Security Considerations](#10-security-considerations-integrated--future-work)
    10.1. [Sandbox Isolation (Docker Dependency Isolation)](#101-sandbox-isolation-docker-dependency-isolation)
    10.2. [Secured Command Execution (`core.linux.executeCommand`)](#102-secured-command-execution-corelinuxexecutecommand)
    10.3. [API Key Management (`ApplicationRegistry`, Validation)](#103-api-key-management-applicationregistry-validation)
    10.4. [Inter-App Communication Permissions (Framework Rules Needed)](#104-inter-app-communication-permissions-framework-rules-needed)
    10.5. [MCP Scoping & Permissions (App Context Enforcement)](#105-mcp-scoping--permissions-app-context-enforcement)
    10.6. [State Access Control (Via `StateManagerInterface`)](#106-state-access-control-via-statemanagerinterface)
    10.7. [Authentication & Authorization (User/Service)](#107-authentication--authorization-userservice)
    10.8. [Prompt Injection / LLM Security](#108-prompt-injection--llm-security)
    10.9. [Secure Deployment](#109-secure-deployment)
11. [Future Work / V2+ Considerations](#11-future-work--v2-considerations)
    11.1. [Advanced State Consistency](#111-advanced-state-consistency)
    11.2. [Enhanced Debugging & Observability](#112-enhanced-debugging--observability)
    11.3. [Security Enhancements](#113-security-enhancements)
    11.4. [Advanced Optimization Logic & Control](#114-advanced-optimization-logic--control)
    11.5. [Enhanced Workflow Capabilities](#115-enhanced-workflow-capabilities)
    11.6. [Performance & Scalability](#116-performance--scalability)
    11.7. [Advanced Caching Strategies](#117-advanced-caching-strategies)
    11.8. [JIT Execution & Reloading Refinements](#118-jit-execution--reloading-refinements)
    11.9. [Framework & MCP API Enhancements](#119-framework--mcp-api-enhancements)
    11.10. [Tooling & User Experience](#1110-tooling--user-experience)
[Glossary](#glossary)
[Appendixes](#appendixes)
    [Appendix A: Example File Structures (Conceptual)](#appendix-a-example-file-structures-conceptual)
    [Appendix B: V0.1 Core MCP Tool Summary](#appendix-b-v01-core-mcp-tool-summary)
    [Appendix C: Protobuf Definitions (Partial Index)](#appendix-c-protobuf-definitions-partial-index)
    [Appendix D: Open Questions / V2+ Areas](#appendix-d-open-questions--v2-areas)

---

## 1. Concept Overview (Reference: UHLP Document Section I)

This section provides a high-level conceptual overview of the Ultra High Level Programming (UHLP) paradigm and the framework designed to support it. UHLP represents a significant shift in how applications are created and executed, moving beyond traditional code generation towards a system where models and dynamic logic *constitute* the runtime itself.

### 1.1. Core Idea: LLM as Runtime

The foundational principle of UHLP is to elevate the programming abstraction significantly above current Very High-Level Languages (VHLLs) such as Python or JavaScript. In the UHLP model, a sophisticated Large Language Model (LLM) or other advanced Generative AI is not merely a tool used to *generate* application code; instead, the **AI model fundamentally acts as the application runtime or service core itself** [1].

This means that for many operational aspects, the LLM directly interprets high-level user intent, manages application state, processes incoming requests, interacts with external tools and data sources (via the Model Context Protocol - MCP), and generates responses or user interface elements dynamically. It becomes the primary engine driving the application's logic and behavior, rather than just a pre-compilation step [1].

### 1.2. Abstraction Layer

UHLP introduces a new layer of abstraction in the software execution stack. Analogous to how Python code runs on an underlying C implementation or Java bytecode executes on a Java Virtual Machine (JVM), UHLP treats the chosen LLM (or a collection of interacting models/JIT components) as the **next-level abstract execution environment** [1].

Developers or users define application behavior using high-level descriptions, prompts, configuration files (YAML), and workflow definitions stored in the application's state [1]. The UHLP Core Framework ingests requests and routes them to the appropriate sandboxed component (which might initially be an LLM) [1]. This component interprets the request in the context of the application's defined state and high-level goals, effectively executing the "program" defined by those high-level descriptions [1]. This shields the user from the complexities of traditional coding for many tasks, allowing them to focus on defining *what* the application should do, relying on the UHLP runtime (LLM + Framework + MCP) to handle *how* it gets done [1].

### 1.3. User Experience Analogy (Roblox-like)

The intended user experience for creating applications with UHLP draws inspiration from platforms like Roblox [1]. The goal is to empower a broader range of users, potentially including those without deep traditional programming expertise, to **define, create, and deploy their own functional applications or interactive digital experiences** [1].

This is achieved primarily through interaction with a user interface (e.g., the Admin Panel) where requirements are specified using natural language prompts, configuration options are selected, and high-level descriptions of desired functionality (including UI elements and logic flows) are provided [1]. The UHLP framework then translates these high-level inputs into the necessary runtime configuration (state files, prompts, workflow definitions) and orchestrates the deployment and execution, aiming for a seamless "description-to-deployment" experience [1].

### 1.4. JIT / Adaptive Nature (Predictive, Reactive, Optimizing)

The UHLP system is designed to be inherently dynamic and adaptive, exhibiting characteristics analogous to Just-In-Time (JIT) compilation in traditional language runtimes [1]. This adaptive nature manifests in several ways:

*   **Predictive:** Based on the initial high-level application description provided by the user during the bootstrap process, the framework proactively generates initial state configurations, component definitions, basic UI templates, and foundational LLM prompts required to get a rudimentary version of the application running [1].
*   **Reactive:** During runtime, as the application handles specific user requests or encounters situations not fully anticipated by the initial configuration, the system (primarily the LLM runtime components) can dynamically generate necessary elements on-the-fly. This could include refining prompts for better results, generating specific data transformations, or even formulating specifications for new JIT code components if performance bottlenecks are identified [1].
*   **Optimizing:** The framework continuously monitors the performance, cost, and correctness of different application components (via the `MetricCollector`) [1]. The `OptimizationOracle` analyzes this data against configurable rules [1]. When predefined thresholds are met (e.g., high latency, high cost, high frequency for an LLM-driven component), the system can automatically trigger a process to generate optimized, persistent code (Just-In-Time compilation to languages like Python or Node.js) [1]. This generated JIT code can then replace the original LLM-interpreted logic for that specific component, transparently improving efficiency without requiring manual refactoring [1]. The system intelligently chooses between the flexibility of direct LLM interpretation and the efficiency of compiled code based on observed runtime behavior and defined optimization goals [1].

---

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
  "requestData": { // Details of the event triggering this execution [1]
    "source": "http" | "trigger" | "callback" | "queue" | "cron" | "internal", // Origin Type [1]
    // --- Conditional based on source ---
    "httpDetails": { // Present if source == 'http' [1]
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
    "triggerDetails": { // Present if source == 'trigger' [1]
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
  "context": { // Background information provided by the Framework [1]
    "appId": "string", // Unique ID of the UHLP application this request belongs to [1]
    "componentId": "string", // ID of the component/workflow being invoked (from state) [1]
    "workflowInfo": { // Optional: Added if handlerType is WORKFLOW
        "workflowId": "string",
        "startAt": "string" // Optional starting step ID
    },
    "mcp_endpoint": "string", // URL for the App-Specific MCP Server the sandbox should use [1]
    "stateConfig": { // Info about how the sandbox should access its state
        "type": "mcp_tool", // Assume state access is primarily via MCP tools initially
        "readTool": "core.state.getDefinitionFileContent",
        "writeTool": "core.state.applyStateDiff" // Tools provided by Core MCP [1]
        // Could potentially support direct volume mounts later
    },
    "userInfo": { // Optional: Present if user context is available/authenticated [1]
      "id": "string",
      "roles": ["string"],
      "isAuthenticated": true,
      "claims": {} // Optional: custom claims/attributes
    },
    "sessionId": "string", // Optional: Identifier for framework-managed session state [1]
    "configuration": { // Select app-specific config values injected by Framework [1]
        /* e.g., "externalApiUrl": "https://partner.com/api" */
    },
    "applicationInfo": { // General info about the running app [1]
        "deploymentMode": "production" | "development" | "staging"
    }
    // Avoid passing sensitive Framework internals directly; use MCP for access [1]
  }
}
```

**Response:**

*   **Success Status Codes (HTTP Layer):**
    *   `200 OK`: Sandbox received the request, processed it (successfully *or* with an *application-level* error defined in the body), and the response body contains the outcome.
*   **Failure Status Codes (HTTP Layer):**
    *   `400 Bad Request`: The request body JSON was malformed or contained invalid structure according to this spec.
    *   `429 Too Many Requests`: (Optional) Sandbox is overloaded and cannot accept the request currently.
    *   `500 Internal Server Error`: The sandbox encountered an *unhandled internal exception* during execution (e.g., coding error in JIT script, internal crash).
    *   `503 Service Unavailable`: The sandbox is temporarily unable to process requests (e.g., cannot connect to essential backend like MCP).
*   **Headers:**
    *   `Content-Type: application/json` (Required on success/application error)
    *   `X-Request-ID: <uuid>` (Required - Echoing the request ID)
*   **Body (on `200 OK`):** JSON payload conforming to the following structure:

```json
{
  "requestId": "string", // Matches request ID
  "resultType": "generic" | "httpResponse" | "error" | "workflowStep", // Type of result [1]
  "data": {
      // --- Structure depends on resultType --- [1]

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

      // Type: "error" - Application-level error identified by sandbox logic [1]
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
  "metrics": { // Optional: Performance metrics from the Sandbox [1]
     "execution_time_ms": 123,
     "mcp_calls": [
       { "tool": "core.state.getFileContent", "count": 2, "total_duration_ms": 15 },
       { "tool": "llm.openai.generate", "count": 1, "total_duration_ms": 95, "token_usage": { "prompt": 300, "completion": 150 } }
     ],
     // Other relevant sandbox-internal metrics
  }
}
```
*   **Body (on HTTP `4xx`/`5xx` Errors):** Optional JSON body providing error details from the sandbox's HTTP server itself.
    ```json
    { "error": "string", "details": "string" }
    ```

---

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
            SandboxPoolConfig sandboxPools = 4; // Requirements for the Sandbox Manager [1]
            StateConfig stateStoreConfig = 5; // How state is stored (e.g., Git repo path) [1]
            ComponentRegistry initialComponentRegistry = 6; // Map of routes/components to handlers [1]
            SecurityConfig securityConfig = 7; // API Keys, inter-app permissions [1]
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
          ResourceLimits resourceLimits = 5; // CPU/Memory limits for containers [1]
          repeated string volumeMounts = 6; // Volume mounts needed (e.g., for code, state access) [1]
        }
        message ResourceLimits { string cpuLimit = 1; /*e.g., "0.5"*/ string memoryLimit = 2; /*e.g., "512M"*/ }
        message StateConfig { string type = 1; /* e.g., "git_yaml" */ map<string, string> params = 2; /* e.g., {"repoUrl": "...", "basePath": "state/"} */ }
        message ComponentRegistry { repeated ComponentDefinition components = 1; }
        message ComponentDefinition {
            string componentId = 1; // Unique ID for this logical component/handler/workflow
            HandlerType handlerType = 2; // LLM, JIT, WORKFLOW [1]
            string targetPoolName = 3; // Which sandbox pool handles this [1]
            map<string, string> taskDetails = 4; // Details specific to the handlerType [1]
                                                 // e.g., { "script": "...", "function": "..." } for JIT
                                                 // e.g., { "prompt_template": "..." } for LLM
                                                 // e.g., { "workflowId": "..." } for WORKFLOW
            string expectedResultFormat = 5; // "generic" | "httpResponse" | "error" [1]
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
            repeated OptimizationRule rules = 2; // Global/App-level rules applied by Oracle [1]
            // Could also include component-level overrides within ComponentDefinition
        }
        message OptimizationRule {
            string description = 1;
            MetricCondition condition = 2; // e.g., latency > 1s AND count > 10/min
            OptimizationAction action = 3; // e.g., TRIGGER_JIT
            map<string, google.protobuf.Value> actionParams = 4; // Params for the action
            bool preferLlmFlexibility = 5; // Hint for the Oracle [1]
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
    *   **Request/Response:**
        *   `Request: { appId, filePath, revision? }`
        *   `Response: { found, content, revision, error? }`
    *   **Implementation:** Uses Git commands (`git show revision:filePath`) or a Git library to retrieve content.

*   **`ApplyDefinitionDiff`**
    *   **Purpose:** **Primary modification method.** Atomically applies a provided patch/diff to a file, ensuring it applies against the expected base revision (optimistic concurrency). Commits the change to Git [1].
    *   **Request/Response:**
        *   `Request: { appId, filePath, diffContent, expectedBaseRevision, commitMessage, author? }`
        *   `Response: { success, resultingRevision, error? }`
    *   **Implementation:** Requires careful implementation: Acquire a lock (e.g., file-based lock, or Redis lock) for the `appId` + `filePath`; clone/pull the repo if necessary; check out `expectedBaseRevision`; attempt to apply the `diffContent` using a patch utility; if successful, commit the change with message/author; push the change (if remote repo); release lock. Handle merge conflicts/patch failures gracefully.

*   **`SetDefinitionFileContent`**
    *   **Purpose:** Overwrites or creates a state file. Should be used cautiously; `ApplyDefinitionDiff` is preferred for modifications [1].
    *   **Request/Response:**
        *   `Request: { appId, filePath, content, commitMessage, author? }`
        *   `Response: { success, resultingRevision, error? }`
    *   **Implementation:** Similar locking/commit/push flow as `ApplyDefinitionDiff`, but overwrites the file content directly.

*   **`DeleteDefinitionFile`**
    *   **Purpose:** Deletes a state file within the Git repository [1].
    *   **Request/Response:**
        *   `Request: { appId, filePath, commitMessage, author? }`
        *   `Response: { success, resultingRevision, error? }`
    *   **Implementation:** Similar locking/commit/push flow, using `git rm`.

*   **`ListDefinitionDirectory`**
    *   **Purpose:** Lists files and subdirectories within the state repository [1].
    *   **Request/Response:**
        *   `Request: { appId, directoryPath, recursive?, revision? }`
        *   `Response: { entries: [{path, type}], revision, error? }`
    *   **Implementation:** Uses Git commands (`git ls-tree`) or library equivalents.

#### 3.3.4. Runtime State Methods (Redis Operations)

These methods interact with the ephemeral key-value store (assumed Redis). Keys are implicitly namespaced by `appId`.

*   **`SetRuntimeValue`**
    *   **Purpose:** Sets or updates a key-value pair, optionally with a TTL [1].
    *   **Request/Response:**
        *   `Request: { appId, key, value: google.protobuf.Value, ttlSeconds? }`
        *   `Response: { success, error? }`
    *   **Implementation:** Connects to Redis, uses `SET` command (with `EX` option if `ttlSeconds` is provided). Value serialization (e.g., JSON for `google.protobuf.Value`) needs to be handled. Keys should be prefixed internally (e.g., `uhlp:runtime:<appId>:<key>`).

*   **`GetRuntimeValue`**
    *   **Purpose:** Retrieves a value by key [1].
    *   **Request/Response:**
        *   `Request: { appId, key }`
        *   `Response: { found, value?: google.protobuf.Value, error? }`
    *   **Implementation:** Uses Redis `GET` command. Handles deserialization from stored format (e.g., JSON) back to `google.protobuf.Value`.

*   **`DeleteRuntimeValue`**
    *   **Purpose:** Deletes a key [1].
    *   **Request/Response:**
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

---

## 4. State Management Details (Reference: UHLP Document Section III)

State management is a cornerstone of the UHLP framework, providing the context, definitions, configuration, and runtime data necessary for applications to function dynamically and adaptively. This section details the conceptual content of the state, the chosen storage mechanisms for different types of state, and how state is accessed via the internal `StateManagerInterface` API.

### 4.1. Conceptual Content

The state associated with a UHLP application encompasses several distinct categories of information, working together to define and drive its behavior:

*   **`ApplicationDefinition`:** The high-level blueprint of the application. This includes metadata (like `appId`, `displayName`, version), configuration for required sandbox pools (`SandboxPoolConfig`), security settings (`SecurityConfig` including API keys and permissions), optimization rules (`OptimizationConfig`), and overall configuration for state storage (`StateConfig`) [1]. This is typically established during application registration via the `ApplicationRegistry` [1].
*   **`ComponentRegistry`:** A critical piece of the definition state, mapping logical application parts or routes to their specific implementations [1]. It typically defines components by `componentId` and includes details like:
    *   The `handlerType` (`LLM`, `JIT`, `WORKFLOW`) [1].
    *   The `targetPoolName` specifying which sandbox pool executes the component [1].
    *   The specific `taskDetails` required by the handler (e.g., prompt template path, JIT script/function name, `workflowId`) [1].
    *   The `expectedResultFormat` (`generic`, `httpResponse`, `error`) [1].
    *   Routing information (`RouteMatcher`) if the component is triggered via HTTP [1].
    *   Component-specific configuration overrides.
    This registry is the primary lookup source for the `RequestRouter` [1] and is updated by the `OptimizationOracle` when JIT code replaces LLM logic [1].
*   **Workflow Definitions:** Declarative YAML files (as specified in Section 6.1) defining multi-step processes, stored within the definition state (e.g., `workflows/my_workflow.yaml`) [1].
*   **Prompt Templates:** YAML files (as specified in Section 8.1) defining the structure and content of prompts used by `LLM` handler types, stored within the definition state (e.g., `prompts/my_prompt.yaml`) [1].
*   **JIT Code Artifacts:** The actual source code files (e.g., `_jit_code/my_component/v1/handler.py`) and potentially associated test files generated by the `OptimizationOracle`, stored within the definition state [1].
*   **`RuntimeData`:** Ephemeral state information relevant during active request processing or short-term application operation [1]. This includes:
    *   Active session information (if using framework-managed sessions).
    *   Temporary variables or intermediate results passed between steps in a complex workflow.
    *   Short-term caching results (though longer-term caching might use dedicated caching MCPs or persisted state).
    *   Distributed locks (e.g., for coordinating access to shared resources or ensuring state file consistency during updates).
*   **`MCPServersConfig`:** Configuration detailing the available Community and Application-Specific MCP servers, their endpoints, and potentially required credentials or routing rules. This information is likely part of the `ApplicationDefinition` or managed configuration accessed via `ApplicationRegistry` [1].
*   **`PerformanceLog` / Metrics:** While raw performance data is handled by the `MetricCollector`, aggregated summaries or historical performance trends relevant for optimization decisions might conceptually be considered part of the application's broader operational state context, informing the `OptimizationOracle` [1].
*   **`OptimizationDecisions`:** A history or log of optimization actions taken by the `OptimizationOracle` (e.g., which components were JIT-compiled when), potentially stored within the definition state for auditability [1].
*   **Application Domain Data:** Data specific to the application's purpose (e.g., user accounts, blog posts, product inventory). **Crucially, this is NOT typically managed by the framework's core state management system.** It resides in external databases (SQL, NoSQL) or object storage, accessed by sandboxes via dedicated **Community MCP Servers** (e.g., `community.database.postgres`, `community.aws.s3`) [1].

### 4.2. Storage Mechanisms

The UHLP framework employs a hybrid storage strategy, choosing appropriate mechanisms based on the nature and requirements of the state data:

#### 4.2.1. Definition/Config State: Git + YAML Files (Primary Source of Truth)

*   **Mechanism:** For the core application definition, configuration, component registry, workflows, prompts, and generated JIT code, the primary storage mechanism is **text files (primarily YAML)** organized within a directory structure specific to the application. This entire directory structure is managed under **Git version control** [1].
*   **Rationale:**
    *   **Versioning & History:** Git provides robust, built-in version tracking, allowing review of changes, rollbacks, and understanding evolution over time [1].
    *   **Traceability & Audit:** Git history inherently logs who made changes and when [1].
    *   **LLM/Tool Processability:** YAML and code files are easily parsed, analyzed, and modified by both LLMs (e.g., for understanding configuration or performing automated upgrades) and standard development tools [1].
    *   **Atomicity (via Commits):** Git commits provide a mechanism for grouping related state changes atomically.
    *   **Branching/Merging:** Git workflows can be used for developing and testing changes to application definitions in isolation.
*   **Access:** Handled via the file-like methods (`GetDefinitionFileContent`, `ApplyDefinitionDiff`, etc.) on the `StateManagerInterface`, which internally interacts with the Git repository [1].
*   **Git LFS:** For potentially large files (e.g., extensive logs if stored in state, large JIT artifacts - though source code is usually small), Git Large File Storage (LFS) can be utilized if necessary, managed transparently by Git [1].

#### 4.2.2. Runtime Ephemeral State: Redis

*   **Mechanism:** For transient `RuntimeData` requiring fast access and potentially supporting atomic operations (like counters or locks), an in-memory data store, **Redis**, is the designated mechanism [1].
*   **Rationale:**
    *   **Performance:** Redis offers extremely fast read/write operations suitable for session data, caching, and runtime variables.
    *   **Atomic Operations:** Provides commands like `INCRBY`, `SETNX` (for locks) that are crucial for reliable runtime coordination.
    *   **TTL Support:** Built-in Time-To-Live features are ideal for managing the lifecycle of ephemeral data like sessions or cache entries.
*   **Access:** Handled via the key-value methods (`SetRuntimeValue`, `GetRuntimeValue`, etc.) on the `StateManagerInterface`, which interacts with the configured Redis instance [1]. Keys are automatically namespaced per `appId`.

#### 4.2.3. Application Domain Data: External Databases (via MCP)

*   **Mechanism:** Data that constitutes the application's core business information (user content, etc.) resides in standard external databases (e.g., PostgreSQL, MongoDB, managed services like Supabase) or object storage (S3) [1].
*   **Rationale:** Separates the application's operational definition (framework state) from its user-generated or business data. Allows leveraging mature, scalable database technologies.
*   **Access:** Sandboxes **do not** access these databases directly. They use standardized **MCP tools** provided by Community MCP Servers (e.g., `community.database.postgres.query`, `community.aws.s3.getObject`) [1]. These MCP servers manage connections and credentials, providing a layer of abstraction and security.

### 4.3. Access API (Provided by `StateManagerInterface`)

All interactions with both Definition/Config state (Git/YAML) and Runtime state (Redis) by framework components or sandboxes (via Core MCP wrappers) **MUST** go through the **`StateManagerInterface` Internal API** (specified in Section 3.3) [1].

This centralized interface provides:
*   **Abstraction:** Callers don't need to know the specifics of Git commands or Redis protocols [1].
*   **Consistency:** Ensures common mechanisms for locking, error handling, and potentially caching are applied.
*   **Security:** Allows centralized enforcement of access controls based on `appId` or other context if needed in the future.
*   **Maintainability:** Changes to underlying storage mechanisms can be implemented within the `StateManagerInterface` without requiring changes in all calling components.

The key methods provided allow reading file content, applying diffs atomically to configuration files, listing directories, and performing standard key-value operations on the runtime store [1].

---

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

---

## 6. Workflow Definition

This section details the structure and capabilities of the **Workflow YAML Definition**, a core concept in UHLP that allows developers to declaratively define complex, multi-step application logic involving various components like LLMs, JIT code, and MCP tools [1]. These definitions are interpreted and executed by an orchestrating component (itself potentially an LLM or a dedicated JIT runner) within a Sandbox [1].

### 6.1. Workflow YAML Structure Specification (Version 1.0)

#### 6.1.1. Purpose & File Location

*   **Purpose:** To provide a standardized, declarative, and version-controlled way to define the sequence of operations, data flow, and control logic for complex tasks within a UHLP application [1]. This replaces the need for hardcoding orchestration logic in many cases, making the application flow more transparent and easier to modify [4].
*   **File Location:** Workflow definitions are stored as standard YAML files within the application's versioned definition state (managed by Git and the `StateManagerInterface`), typically located in a dedicated subdirectory like `workflows/` (e.g., `workflows/process_new_order.yaml`) [1].

#### 6.1.2. Top-Level Properties

Each Workflow YAML file has the following key properties at the root level:

```yaml
# Unique identifier for this specific workflow definition. Must be unique within the application.
# Used by the ComponentRegistry to map triggers (like HTTP routes) to this workflow.
workflowId: process_new_order_v1

# Optional: A human-readable description explaining the purpose and function of the workflow.
description: Validates incoming order data, processes payment via Stripe MCP, updates inventory via DB MCP, and notifies the user.

# Defines the event(s) that can initiate this workflow.
trigger:
  # Specifies the source type, aligning with requestData.source (e.g., http, queue, cron, trigger).
  type: http
  # Configuration specific to the trigger type.
  config:
    # For 'http' triggers, defines the route matching criteria used by RequestRouter.
    pathPattern: /api/v1/orders
    method: POST

# Specifies the ID of the first step where workflow execution should begin.
startAt: validate_order_schema

# Map defining all the individual steps that make up the workflow.
# The keys of this map are the unique step IDs used for identification and transitions.
steps:
  # ... detailed step definitions follow ...
```

#### 6.1.3. Step Definition (`stepId`, `type`, `target`, `inputMapping`, `transitions`)

Within the `steps:` map, each key is a unique identifier (`stepId`) for a step within the workflow. The associated value is an object describing the step's configuration:

```yaml
steps:
  # Example Step ID
  validate_order_schema:
    # Required: Specifies the type of action this step performs.
    # Supported V1 types: jit, llm, mcp, control [1]
    type: jit
    # Optional: Human-readable description of the step's purpose.
    description: Validate the incoming order payload against the required JSON schema.
    # Required (for most types): Defines the specific resource or action being invoked.
    # Structure varies based on 'type'.
    target:
      # For 'jit' type:
      language: python # Specifies the required JIT runner language/pool [1]
      script: "_jit_code/validators/order_validator.py" # Path to the JIT script file [1]
      function: "validate_schema" # Function within the script to execute
    # Required: Defines how to construct the input data for this step.
    # Uses the Workflow Expression Syntax (see 6.1.5) to map data from the trigger or previous steps.
    inputMapping:
      orderData: trigger.requestData.httpDetails.body # Pass the parsed HTTP body
      schemaPath: "'schemas/order_schema.v1.json'" # Pass a static path as a literal string
    # Required: Defines the control flow after this step completes.
    # Specifies where to go next based on success or failure, potentially using conditions.
    transitions:
      # If the step executes successfully, proceed to the 'process_payment' step.
      onSuccess: process_payment
      # If the step fails (e.g., validation error), proceed to 'format_validation_error'.
      onFailureDefault: format_validation_error
```

#### 6.1.4. Step Types (`jit`, `llm`, `mcp`, `control`)

The `type` property determines the fundamental action performed by a step:

*   **`jit`:** Executes a predefined function within a JIT code script [1].
    *   `target`: Must specify `language`, `script` path, and `function` name.
    *   **Execution:** The workflow orchestrator packages the inputs defined by `inputMapping` and uses an MCP call (back to the framework/`RequestRouter`) to request execution of this specific JIT function in an appropriate sandbox pool. The result is returned via the MCP response [1].
*   **`llm`:** Interacts with a Large Language Model [1].
    *   `target`: Must specify `promptTemplate` (path to a YAML prompt template file, see Section 8.1) or inline `prompt`. Can optionally override `model` and LLM `parameters`.
    *   **Execution:** The orchestrator loads the prompt template (if specified), renders it using Jinja2 and inputs from `inputMapping`, then calls the `core.llm.generate` MCP tool [1]. The validated (against `outputSchema` if provided) LLM response becomes the step's output [1, 2].
*   **`mcp`:** Directly invokes a tool available via the Model Context Protocol [1].
    *   `target`: Must specify the full `tool` name (e.g., `community.database.postgres.query`, `core.linux.executeCommand`).
    *   **Execution:** The orchestrator formats the parameters based on `inputMapping` and makes the specified MCP tool call via its `mcp_endpoint`. The result of the MCP call becomes the step's output [1].
*   **`control`:** Performs internal workflow logic or data manipulation without external calls [1]. Requires a `subtype` for specific behavior:
    *   `formatResponse`: (V1) Prepares the final data structure to be returned as the overall workflow result, defining the `resultType` and `data` for the `RequestRouter` [1]. Should have `transitions: { end: true }`.
    *   **(Future/V2 Placeholders inspired by n8n [1]):**
        *   `loop`: Iterates over a list provided via `inputMapping`, executing a specified sub-step (or inline definition) for each item. Needs structure for input list, item variable name, loop body step(s).
        *   `branch`: Explicit multi-way conditional branching based on `condition` expressions, directing flow to different next steps.
        *   `merge`: Defines how to combine data from multiple incoming branches (relevant after `branch` or `parallel`). Needs strategies (e.g., append, merge objects).
        *   `split`: Distributes processing based on conditions or item types.
        *   `wait`: Pauses workflow execution (e.g., for a fixed duration, until a specific time, until an external event/webhook is received via framework).
        *   `subworkflow`: Calls another `workflowId` as a self-contained unit, passing inputs and receiving outputs.

#### 6.1.5. Expression Syntax (V1 - Simple JSONPath-like / Dot Notation)

A simple expression syntax is used within `inputMapping` (to define data sources) and `transitions` `condition`s (to evaluate boolean logic) [1].

*   **Data Access:** Uses dot notation to access data originating from:
    *   `trigger.*`: The initial event data (structure depends on `trigger.type`, mirroring `requestData`) [1].
    *   `steps.<stepId>.output.*`: The entire output object of a previously executed step [1]. Can access nested properties (`steps.stepA.output.user.address.city`). Array access via index (`steps.stepB.output.results[0]`).
    *   `step.output.*`: Within `transitions`, accesses the output of the *current* step (useful for checking success/failure details or immediate output values) [1].
    *   `context.*`: Data from the `context` object provided in the initial `/execute` call (`context.userInfo.id`, `context.configuration.someKey`) [1].
    *   `workflow.*`: (TBD V1/V2) Workflow-level context like `workflow.id`, `workflow.startTime`, potential shared variables, `workflow.lastError`.
*   **Literals:** String literals must be enclosed in single quotes (`'hello'`, `'SELECT *'`). Numbers (`123`, `0.5`) and booleans (`true`, `false`) are used directly [1].
*   **Conditions (`condition` field):** Support basic comparisons (`==`, `!=`, `>`, `<`, `>=`, `<=`) and logical operators (`&&` - AND, `||` - OR, `!` - NOT). Parentheses `()` can be used for grouping. An existence check function `defined(path.to.optional.field)` might be useful [1].
*   **Scope:** Expressions assume data is JSON-like. V1 focuses on basic retrieval and boolean logic. More complex transformations (string manipulation, array filtering) might require a dedicated `jit` step or richer expression functions in V2 [1].

#### 6.1.6. Transitions & Flow Control (`onSuccess`, `onFailure`, `condition`, `end`)

The `transitions` block within a step definition dictates the workflow's execution path after the step completes [1].

*   **Evaluation Order:** If multiple conditional transitions are defined (e.g., within `onFailure` or as a list under `transitions`), they are evaluated sequentially. The first condition that evaluates to `true` determines the `nextStep`.
*   **Success Path (`onSuccess`):** A shorthand specifying the `stepId` to transition to if the current step completes successfully (e.g., JIT function returns non-error, MCP call succeeds, LLM call returns valid output).
*   **Failure Handling (`onFailure`, `onFailureDefault`):**
    *   `onFailure`: An optional list of conditional transitions specifically for handling *internal failures* within the step execution (e.g., JIT code throws exception, MCP tool returns error, LLM validation fails). Each entry requires a `condition` (often referencing `step.output.error.*`) and a `nextStep`.
    *   `onFailureDefault`: Specifies the `stepId` to transition to if the step fails internally *and* no `onFailure` condition matched. If omitted and failure occurs, workflow execution may halt with an error.
*   **Unified `transitions` Array (Alternative/Preferred Structure):**
    ```yaml
    transitions:
      # Example: Conditional success path
      - condition: step.output.result.needsReview == true
        nextStep: flag_for_manual_review
      # Example: Default success path (condition omitted)
      - nextStep: update_status_complete
      # Example: Specific failure handling
      - condition: defined(step.output.error) && step.output.error.code == 'TIMEOUT'
        nextStep: handle_timeout_error
      # Example: Default failure path (condition omitted, evaluated after specific failures)
      - nextStep: handle_generic_step_failure
    ```
    This array structure provides more flexibility than separate `onSuccess`/`onFailure` blocks.
*   **Ending the Workflow (`end: true`):** A transition target of `end: true` signifies that the workflow execution should terminate after this step. Terminal steps (both success and error handling paths) must include this in their transitions [1]. The output of the final step before `end: true` typically becomes the overall result provided back to the `RequestRouter` (especially if formatted by a `control.formatResponse` step).

### 6.2. Execution Model

1.  The `RequestRouter` identifies that a trigger matches a `WORKFLOW` handler type [1].
2.  It allocates an appropriate orchestrator sandbox (JIT Runner or LLM) and sends the `/execute` call, including `context.workflowInfo { workflowId }` [1].
3.  The orchestrator sandbox receives the call, extracts the `workflowId`, and loads the corresponding Workflow YAML file using `core.state.getDefinitionFileContent` [1].
4.  It starts execution at the step defined by `startAt` [1].
5.  For each step:
    *   It resolves inputs using `inputMapping` and the current data context (trigger + previous step outputs).
    *   It executes the step based on its `type` (invoking JIT via MCP, calling LLM via MCP, calling MCP directly, or processing control logic) [1].
    *   It stores the step's output.
    *   It evaluates the `transitions` block to determine the `nextStep` ID [1].
6.  Execution continues until a step transitions to `end: true` [1].
7.  The output of the final step is formatted and returned as the result of the initial `/execute` call [1].

### 6.3. Enhancements Inspired by n8n (V2+ Considerations)

While V1 focuses on the core structure, future versions should incorporate more advanced flow control and data handling concepts inspired by mature tools like n8n [1]:
*   **Robust Looping:** Implementing dedicated `loop` constructs [1].
*   **Parallel Execution:** Adding a `parallel` step/block to run multiple branches concurrently.
*   **Advanced Merging/Splitting:** Defining explicit strategies for handling data across branches [1].
*   **Subworkflows:** Allowing workflows to call other workflows modularly [1].
*   **Sophisticated Error Handling:** Implementing configurable retries, dead-letter queues, `try/catch`-like blocks within the YAML [1].
*   **Wait States:** Adding explicit `wait` steps for timed delays or external event triggers [1].
*   **Richer Expression Language:** Enhancing the expression syntax with more built-in functions for data transformation [1].
*   **Item Linking / Context:** More explicit ways to manage data context across iterations or branches [1].

---

## 7. Dynamic Execution & Optimization (Reference: UHLP Document Section V)

A defining characteristic of the UHLP framework is its ability to dynamically adapt and optimize its execution strategy over time [1]. Instead of relying solely on static code or fixed configurations, the system continuously monitors its performance and can transparently switch between different execution modes (such as direct LLM interpretation and Just-In-Time compiled code) to meet performance goals, cost constraints, or administrative preferences [1]. This section details the mechanisms enabling this dynamic behavior.

### 7.1. Runtime Decision Making (Handled by `OptimizationOracle`)

The core intelligence behind the optimization process resides within the **`OptimizationOracle`** component (specified in Section 3.6) [1]. This component is responsible for analyzing runtime data and deciding when and how to optimize specific parts of a UHLP application [1].

*   **Data Source:** The `OptimizationOracle` primarily relies on operational metrics aggregated by the **`MetricCollector`** (specified in Section 3.5) [1]. It queries for metrics like execution latency, LLM token consumption (which translates to cost), frequency of component execution (throughput), and error rates, typically grouped by application (`appId`) and logical component (`componentId`) [1].
*   **Analysis & Triggering:** For components currently executed via LLM interpretation (`handlerType == 'llm'`), the Oracle evaluates the collected metrics against a set of **configurable rules** [1]. These rules, defined globally, per-application, or even per-component within the `ApplicationDefinition` state (managed via `ApplicationRegistry` and potentially the Admin Panel) [1], specify thresholds or conditions under which optimization should be considered.
    *   *Example Rules:* Trigger JIT if latency exceeds 1 second, if cost per call surpasses $0.01, or if call frequency is very high [1].
*   **Configurable Control & Flexibility:** The decision process is not purely automatic. Administrators can configure the rules via the Admin Panel, including setting flags like `prefer_llm_for_flexibility` to prevent automatic JIT compilation for components where the dynamic nature of the LLM is valued over raw performance [1]. The Oracle respects these configurations, potentially generating recommendations instead of automatically triggering JIT for certain components [1]. Manual triggers via the Admin Panel can also bypass the rules to force optimization [1].
*   **Outcome:** Based on rule evaluation or manual triggers, the `OptimizationOracle` decides whether to initiate the JIT code generation process for a specific component [1].

### 7.2. Execution Paths (LLM vs. JIT)

As a result of the initial application definition and subsequent optimizations, a component within a UHLP application can be executed via different paths:

*   **LLM Execution Path:** The component is defined with `handlerType: llm`. The `RequestRouter` identifies this and allocates an appropriate LLM runner/orchestrator sandbox [1]. The sandbox loads the prompt template, renders it, calls the `core.llm.generate` MCP tool, and processes the response [1]. This path offers maximum flexibility and allows leveraging the latest LLM capabilities but may incur higher latency and cost [1].
*   **JIT Execution Path:** After the `OptimizationOracle` initiates and completes the JIT process for a component, the `ComponentRegistry` state is updated to `handlerType: jit` with `taskDetails` pointing to the generated script file [1]. The `RequestRouter` then identifies this and allocates a JIT runner sandbox for the appropriate language [1]. The sandbox receives the `/execute` call and, using the V0.1 "Interpreter Mode", invokes the specified script file (available via shared volume) directly using the language interpreter [1]. This path typically offers lower latency and cost for frequently executed, well-defined tasks but might be less flexible than direct LLM interpretation [1].

The `RequestRouter` seamlessly directs traffic to the currently designated execution path based on the up-to-date `ComponentRegistry` state, making the switch between LLM and JIT execution transparent to the calling client or workflow step [1].

### 7.3. JIT Code Generation Workflow (Detailed within `OptimizationOracle`)

When the `OptimizationOracle` decides to generate JIT code for a component (based on Section 7.1), it orchestrates the following workflow [1]:

1.  **Specification Formulation:** It retrieves the current definition of the component (e.g., the LLM prompt template and observed input/output patterns) from the `StateManagerInterface` [1]. It analyzes this information to create a detailed specification for the equivalent functionality in the target JIT language (e.g., Python, configured per-app). This spec includes function signatures, input data types, expected output structure (potentially using `outputSchema` from the prompt template), and key logic requirements [1].
2.  **Coder LLM Invocation:** The Oracle uses the `core.llm.generate` MCP tool to invoke a specialized "Coder LLM" known for high-quality code generation (e.g., Claude 3 Opus, GPT-4 variants) [1]. It provides the detailed specification formulated in the previous step as the prompt, explicitly requesting both the optimized code implementation *and* accompanying unit tests/test data to help ensure correctness [1].
3.  **Artifact Storage:** Upon receiving the generated code and tests from the Coder LLM, the `OptimizationOracle` uses the `StateManagerInterface.SetDefinitionFileContent` method (or `ApplyDefinitionDiff`) to write these artifacts to a designated location within the application's versioned definition state (e.g., `_jit_code/<componentId>/<version>/handler.py`, `_jit_code/<componentId>/<version>/test_handler.py`) [1]. This action ensures the new code is persisted and becomes available via the shared volume mounts used by the JIT runner sandboxes [1].
4.  **State Update (Routing Change):** After successfully storing the artifacts, the Oracle performs the final crucial step: it calls `StateManagerInterface.ApplyDefinitionDiff` to modify the application's `ComponentRegistry` state [1]. This diff updates the entry for the specific `componentId`, changing its `handlerType` to `jit` and updating the `taskDetails` to point to the newly saved script path and function name [1].
5.  **Activation:** Because V0.1 uses the "Interpreter Mode" for JIT execution and removes the `HotReloadManager`, no further explicit action is needed to "load" the code [1]. The state update in the `ComponentRegistry` is sufficient. The next time the `RequestRouter` handles a request for this `componentId`, it will see the `handlerType: jit`, allocate a JIT runner sandbox, and the sandbox will execute the *new* script file referenced in the updated `taskDetails`, effectively activating the optimized path [1].

### 7.4. Multi-Layer Caching (Concept - Not Specified in Detail for V1)

The UHLP Concept document (Section V) also mentions the idea of multi-layer caching, including caching prompts (base or enhanced), JIT code snippets, and final outputs [1]. While caching is a vital optimization technique, the specific mechanisms, storage (potentially using `StateManagerInterface` runtime state methods or dedicated caching MCPs), and invalidation strategies (noted as complex, potentially LLM-managed [1]) are **not specified in detail for V0.1** and are considered **future work (V2+)**. Basic caching might occur implicitly at various layers (e.g., LLM provider caching), but a sophisticated, framework-managed multi-layer cache requires further design.

---

## 8. Prompt Template Format

LLM Prompts are a fundamental part of defining application logic within the UHLP framework, especially for components using the `LLM` handler type or workflows invoking LLMs [1]. This section specifies the standard format for storing and defining these prompts within the application's state directory, enabling dynamic data injection, metadata management, and structured output expectations [1].

### 8.1. LLM Prompt Template Format Specification (Version 1.0)

#### 8.1.1. Purpose & File Format (YAML)

*   **Purpose:** To provide a standardized, version-controlled format for defining LLM prompts used by UHLP applications. This format facilitates dynamic generation of prompts based on runtime context, allows association of important metadata, and enables specification of desired output structures for improved reliability [1, 2].
*   **File Format:** Prompt templates are defined using **YAML** files [1].
*   **Location:** These YAML files reside within the application's versioned definition state (managed by Git and the `StateManagerInterface`), typically organized in a dedicated subdirectory like `prompts/` (e.g., `prompts/summarize_customer_interaction.yaml`) [1].

#### 8.1.2. Structure (Metadata + `template`)

Each prompt template YAML file follows a structured format, incorporating both the core prompt text and associated metadata [2]:

```yaml
# --- Example: prompts/summarize_customer_interaction.yaml ---

# Optional: Human-readable string describing the prompt's objective.
description: Summarizes a customer interaction transcript, extracting key points and sentiment.

# Optional: Allows overriding the application's default LLM model specifically for this prompt.
# If omitted, the model configured globally for the application (via ApplicationRegistry) is used.
# Example values: "gpt-4-turbo", "claude-3-sonnet", "gemini-1.5-pro"
model: "claude-3-haiku"

# Optional: Default parameters to use for the LLM API call when using this template.
# These parameters can be further overridden by values provided dynamically in the workflow step
# that invokes this prompt. Common LLM parameters include temperature, max_tokens, top_p, etc.
parameters:
  temperature: 0.6
  max_tokens: 500

# Required: The core prompt template string itself. This field contains the text that will be
# processed by the templating engine and sent to the LLM.
template: |
  # --- (Content of the template field below) ---
  Role: You are an AI assistant specialized in analyzing customer support interactions.
  Task: Analyze the following interaction transcript and provide a summary according to the specified JSON format.

  Transcript:
  ```
  {{ interaction_transcript }}
  ```

  {% if customer_history %}
  Additional Customer History Context:
  - Loyalty Status: {{ customer_history.loyalty_status | default('N/A') }}
  - Recent Issues: {{ customer_history.recent_issues_count | default(0) }}
  {% endif %}

  Instructions:
  1. Read the transcript carefully.
  2. Identify the main reason for the customer contact.
  3. Determine the overall sentiment of the customer (positive, neutral, negative).
  4. Extract any specific action items or follow-ups mentioned.
  5. Generate a concise summary (2-3 sentences).

  Output Format: Respond ONLY with a valid JSON object containing the keys "main_reason", "sentiment", "action_items", and "summary".

# Optional: A hint indicating the expected format of the LLM's completion text.
# Common values: "json", "text", "xml", "yaml". This helps the framework or orchestrator
# anticipate how to parse or validate the LLM's response. [2]
outputFormat: json

# Optional: A formal JSON Schema definition describing the expected structure and data types
# of the LLM's output, particularly used when outputFormat is "json". [2]
# This schema enables automatic validation of the LLM's response by the framework/orchestrator
# before it's used in subsequent workflow steps, increasing reliability.
outputSchema:
  type: object
  properties:
    main_reason":
      type: string
      description: "The primary reason the customer initiated contact."
    sentiment:
      type: string
      enum: ["positive", "neutral", "negative"]
      description: "The overall sentiment expressed by the customer."
    action_items":
      type: array
      items:
        type: string
      description: "A list of specific action items or follow-ups required."
    summary:
      type: string
      description: "A concise 2-3 sentence summary of the interaction."
  required:
    - main_reason
    - sentiment
    - action_items
    - summary

# Optional (Future V2+): A list of few-shot examples to improve LLM performance for complex tasks.
# Structure TBD, could be a list of objects, each containing example 'input_vars' and the corresponding 'expected_output'.
# examples:
#   - input_vars: { interaction_transcript: "...", customer_history: {...} }
#     expected_output: '{ "main_reason": "Billing query", "sentiment": "neutral", ... }'
```

#### 8.1.3. Templating Engine (Jinja2)

The `template` field within the YAML file is processed using the **Jinja2 templating engine** before being sent to the LLM [2]. This provides powerful capabilities beyond simple variable substitution:

*   **Variable Injection:** Dynamically insert data into the prompt using `{{ variableName }}` syntax [2]. Variables are sourced from the `inputMapping` defined in the workflow step or component that invokes this prompt template [1]. Nested data access (e.g., `{{ user.profile.email }}`) is supported.
*   **Conditionals:** Include logic within the prompt using `{% if condition %} ... {% elif condition %} ... {% else %} ... {% endif %}` blocks [2]. Conditions can reference context variables.
*   **Loops:** Iterate over lists or sequences using `{% for item in item_list %} ... {% endfor %}` blocks, useful for formatting lists of data or examples within the prompt [2].
*   **Filters:** Apply transformations to variables using standard Jinja2 filters (e.g., `{{ data | tojson }}`, `{{ text | upper }}`, `{{ value | default('N/A') }}`) and potentially custom filters defined by the framework [2].
*   **Markdown Compatibility:** The content within the `template` string can utilize Markdown formatting (headers, lists, code blocks, etc.). This Markdown is rendered as part of the final prompt string sent to the LLM, which can often interpret it effectively for structuring instructions or data presentation.

#### 8.1.4. Output Specification (`outputFormat`, `outputSchema`)

To improve the reliability and predictability of LLM interactions, the template format allows specifying expectations about the LLM's output:

*   **`outputFormat`:** A simple string hint (e.g., `"json"`, `"text"`) indicating the expected general format of the LLM's completion [2]. This can guide subsequent parsing steps.
*   **`outputSchema`:** For structured outputs (especially JSON), this field allows defining a formal **JSON Schema** [2]. When present, the UHLP framework component (e.g., the workflow orchestrator or MCP wrapper) receiving the LLM's response SHOULD attempt to parse the completion according to the `outputFormat` and then validate the resulting data structure against this schema [2]. Validation failures can be treated as errors, preventing malformed data from propagating through the system and potentially triggering error handling or retry logic.

#### 8.1.5. Processing Flow Summary

1.  A workflow step (`type: llm`) or direct component invocation identifies a `promptTemplate` file path [1].
2.  The orchestrator/runner loads the YAML file (via `core.state.getDefinitionFileContent`) [1].
3.  It prepares the Jinja2 context dictionary based on the `inputMapping` [1].
4.  It renders the `template` string using Jinja2 [2].
5.  It constructs the final payload for the `core.llm.generate` MCP tool, including the rendered prompt, effective model, and merged parameters [1].
6.  It invokes the MCP tool [1].
7.  Upon receiving the LLM completion, it optionally parses and validates the output against `outputFormat` and `outputSchema` [2].
8.  The (potentially validated) result becomes the output of the LLM step/component [1].

---

## 9. UI & Application Lifecycle (Reference: UHLP Document Section VI & VII)

This section describes how User Interfaces (UIs) for UHLP applications are generated and served, outlines the process for creating and deploying new UHLP applications (the bootstrap process and lifecycle), and touches upon the requirements for the administrative interface used to manage the framework and applications.

### 9.1. UI Generation

A key aspect of the UHLP paradigm is the dynamic generation of user interfaces based on the high-level application definition and runtime interactions.

*   **Generation Mechanism:** For the initial versions (V0.1/V1), the primary mechanism for UI generation involves an **LLM** (either the main application LLM handler or a specialized UI-focused LLM invoked via an MCP tool or workflow step) [1]. Based on the application's definition (`ApplicationDefinition`, `ComponentRegistry`), user requirements specified during bootstrapping, and potentially the context of the current request, the LLM generates standard web frontend code: **HTML, CSS, and JavaScript** [1].
*   **Simplicity Focus:** The initial focus is on generating functional, standard interfaces rather than highly complex or unique frontend architectures. Standard layouts, form elements, and basic interactivity driven by JavaScript making calls back to the UHLP application's backend endpoints (routed via the `RequestRouter`) are expected.
*   **State-Driven:** The UI structure and content should reflect the current state and capabilities defined in the `ComponentRegistry` and Workflow Definitions. As the application logic evolves (e.g., through JIT optimization or definition changes), the UI generation logic should ideally adapt, though the specifics of maintaining this synchronization are complex and may evolve past V1.
*   **Serving:** The generated static assets (HTML, CSS, JS files) or dynamically rendered HTML are served directly by the **UHLP Core Framework** itself [1]. The framework needs an integrated web server component capable of handling HTTP GET requests for UI assets and routing backend API calls (typically starting with `/api/` or similar prefix) to the `RequestRouter`.

### 9.2. Bootstrap Process (Application Creation)

This describes the sequence of events initiated by a user (typically an administrator or developer) to create and deploy a new UHLP application using the framework. This process heavily involves the Admin Panel and the `ApplicationRegistry` [1].

1.  **User Interaction (Admin Panel):** The user interacts with a dedicated section within the UHLP **Admin Panel** designed for creating new applications [1].
2.  **Application Definition Input:** The user provides the necessary inputs to define the new application [1]:
    *   **Natural Language Description:** High-level description of the application's purpose and intended functionality.
    *   **Application ID / Name:** A unique identifier and display name.
    *   **Configuration Selection:** Choosing required Community MCP servers (e.g., selecting a Postgres database integration), specifying target LLM providers/models, potentially setting initial optimization rules or preferences (`preferLlmFlexibility`) [1].
    *   **API Keys / Credentials:** Securely providing necessary API keys or credentials required for selected MCP integrations or LLM access (these need to be stored securely, likely managed by the framework and referenced via configuration, not directly in versioned state) [1].
    *   **Basic UI Preferences:** Potentially selecting basic options like "Include a landing page," "Use standard login flow," etc [1].
3.  **Framework Processing (`ApplicationRegistry.RegisterApplication`):** Upon user submission, the Admin Panel backend triggers a call to the **`ApplicationRegistryService.RegisterApplication`** method [1]. This involves:
    *   **Translating Input:** A framework component (potentially involving an LLM itself in a meta-role) translates the user's high-level descriptions and selections into the formal `AppDefinition` structure (specified in Section 3.1.5) [1]. This includes generating:
        *   The initial `ComponentRegistry` based on inferred endpoints and functionality.
        *   Initial Workflow Definition YAML files for core processes (if derivable).
        *   Initial LLM Prompt Template YAML files.
        *   The `SandboxPoolConfig` specifying required runner types (e.g., an LLM orchestrator pool).
        *   The `StateConfig`, defining how the state repository should be set up (e.g., initialize a Git repository at a specific path).
        *   The `SecurityConfig`, storing hashed API keys and initial permissions.
    *   **State Initialization:** The `StateManagerInterface` (invoked by the `ApplicationRegistry`) initializes the application's definition state storage (e.g., creates the Git repository, commits the initial set of generated YAML files) [1].
    *   **Registration:** The `ApplicationRegistry` formally registers the `appId` and stores its `AppDefinition` [1].
4.  **Resource Provisioning (`SandboxManager`):** The registration event (or subsequent polling by the `SandboxManager`) triggers the `SandboxManager` [1]:
    *   It calls `ApplicationRegistryService.GetSandboxRequirements` for the new `appId` [1].
    *   Based on the requirements, it interacts with Docker to pull necessary images and start the initial pool(s) of Sandbox containers for the application [1].
5.  **Application Activation:** Once the state is initialized and the initial sandbox pool is running, the `ApplicationRegistry` marks the application status as `Active` [1]. The application is now ready to receive requests.

### 9.3. Deployment & Access

Once an application is bootstrapped and active, the framework provides mechanisms for accessing it:

*   **Shareable Subdomain:** The Core Framework (likely in conjunction with ingress routing configured above it) automatically assigns and routes traffic from a **unique subdomain** (e.g., `my-todo-app.uhlp.example.com`) to the specific UHLP application (`appId`) managed internally [1]. The framework's initial request handling layer uses the hostname (or other identifiers like API keys in headers) to identify the target `appId` before passing the request to the `RequestRouter`.
*   **Access Control:** Basic access control flags can be associated with the application, potentially managed via the `ApplicationDefinition` state and the Admin Panel [1]. This could include:
    *   A simple global on/off switch for the application's public accessibility.
    *   Flags to restrict access during development or testing (e.g., requiring specific authentication or IP address ranges). More granular access control would rely on authentication/authorization logic within the application's components or workflows, potentially using user roles defined in `SecurityConfig` [1].

### 9.4. Admin Panel Requirements (V1 Sketch)

While not a core runtime component, a functional **Admin Panel** is essential for managing the UHLP framework and the applications it hosts. V1 requirements include:

*   **Application Management:**
    *   UI for initiating the **Bootstrap Process** (creating new applications) as described in Section 9.2 [1].
    *   Listing deployed applications with their current status (`Active`, `Inactive`, `Error`) obtained via `ApplicationRegistryService.GetApplicationStatus` [1].
    *   Viewing key details of an application's definition (`ApplicationRegistryService.GetApplicationDetails`) [1].
    *   Triggering application updates (invoking `ApplicationRegistryService.UpdateApplication` after modifying configuration via the UI) [1].
    *   Activating/Deactivating or Deregistering applications (invoking `ApplicationRegistryService.DeregisterApplication`) [1].
*   **Basic Monitoring:** Displaying key metrics sourced from the `MetricCollector` (via Prometheus scraping or a direct API), such as request counts, latency, error rates, and LLM token usage per application [1, 4].
*   **Optimization Control:**
    *   UI for viewing and configuring optimization rules (Global, Per-App, Per-Component) that are stored within the `AppDefinition` state [1].
    *   Displaying recommendations generated by the `OptimizationOracle` [1].
    *   A button/mechanism to manually trigger the JIT optimization process for a specific component (calling the relevant internal API) [1].
*   **Configuration Management:** UI for managing global framework settings and potentially sensitive application configurations (like API keys, although secure storage is paramount).
*   **(Potential V1/V2) State Viewing/Editing:** Limited capability to browse or perhaps even carefully edit the YAML files in the application's definition state (via `StateManagerInterface` calls), primarily for debugging or advanced configuration.

The Admin Panel acts as the primary human interface for interacting with the framework's control plane, utilizing the internal APIs (especially `ApplicationRegistryService`) extensively.

---

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
*   **Strict Whitelisting:** Execution is restricted to commands explicitly listed on an **application-specific whitelist** [1]. This whitelist contains full paths to executables (e.g., `/usr/bin/jq`, `/usr/local/bin/curl-wrapper`) and is managed via application configuration (`ApplicationRegistry`). Attempting to execute any command not precisely matching the whitelist MUST fail immediately [1]. Path manipulation must be prevented.
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

---

## 11. Future Work / V2+ Considerations

While the specifications outlined in the preceding sections define a functional V0.1/V1 UHLP framework, numerous areas offer potential for enhancement, refinement, and the addition of more sophisticated capabilities in future iterations (V2 and beyond). This section captures key considerations deferred from the initial implementation.

### 11.1. Advanced State Consistency

*   **Challenge:** The V1 reliance on file locking (`StateManagerInterface` internal logic) for Git/YAML updates and the basic nature of Redis transactions provide reasonable but not bulletproof consistency guarantees, especially under high concurrency or in distributed scenarios [1].
*   **Future Work:** Implementing more robust distributed consensus mechanisms (e.g., Raft, Paxos if state management becomes distributed, or leveraging distributed locking services like ZooKeeper/etcd if needed) or adopting storage backends with stronger transactional guarantees (potentially sacrificing pure Git/YAML for certain state aspects) might be necessary for mission-critical applications requiring higher consistency levels. Investigating Conflict-free Replicated Data Types (CRDTs) could also be relevant if merging concurrent state changes becomes a primary concern.

### 11.2. Enhanced Debugging & Observability

*   **Challenge:** Debugging applications where logic dynamically shifts between LLM interpretation and JIT code, orchestrated by declarative workflows, presents unique challenges compared to traditional applications [1]. V1 relies on basic logging (`core.framework.logFrameworkMessage`) and metrics (`MetricCollector`).
*   **Future Work:** Developing specialized tools and techniques is crucial [1]. This could include:
    *   Visual workflow execution tracing (similar to n8n's UI [1]) showing data flow and step status in real-time or post-mortem.
    *   Integrated logging views within the Admin Panel, correlating logs across framework components, sandboxes, and MCP calls for a single request trace.
    *   Time-travel debugging capabilities, allowing inspection of state and inputs at specific workflow steps.
    *   Mechanisms for breakpointing and inspecting data within workflow executions (potentially challenging in a distributed sandbox environment).
    *   Enhanced metrics and tracing compliant with standards like OpenTelemetry Tracing [3] for better distributed system visibility.

### 11.3. Security Enhancements

*   **Stronger Sandboxing:** Evaluate and potentially implement stricter sandbox isolation mechanisms like **Firecracker microVMs** [4] if running untrusted code or providing strong multi-tenant guarantees becomes a requirement, moving beyond Docker's shared kernel limitations [1].
*   **LLM-Managed MCP Security:** Defining robust security models for dynamically created/managed LLM-MCP servers [1]. How are their capabilities constrained? How is their lifecycle managed securely?
*   **Custom Security LLMs:** Training or fine-tuning specialized LLMs focused on security analysis (e.g., reviewing generated JIT code for vulnerabilities, analyzing prompt injection attempts, evaluating generated infrastructure configurations) [1].
*   **Advanced Input/Output Sanitization:** Implementing more sophisticated techniques for detecting and mitigating prompt injection in user inputs and sanitizing potentially harmful outputs from LLMs before they are used by other components.
*   **Formal Verification:** Exploring possibilities for formally verifying parts of the framework logic or generated JIT code, especially for critical components.

### 11.4. Advanced Optimization Logic & Control

*   **Sophisticated Oracle:** Enhancing the `OptimizationOracle` with more advanced analysis capabilities beyond simple rule-based thresholding [1]. This could involve:
    *   Using machine learning models to predict performance/cost impacts of JIT compilation more accurately.
    *   Performing more detailed cost modeling based on specific LLM pricing and resource usage.
    *   Considering component dependencies and call graph structure during optimization decisions.
*   **Dynamic Rollback:** Implementing mechanisms for the `OptimizationOracle` or `SandboxManager` to automatically detect if a newly deployed JIT component is performing worse (higher errors, unacceptable latency) than the LLM version and automatically roll back the routing state (`ComponentRegistry`) to the previous version [1].
*   **A/B Testing Optimizations:** Allowing canary deployments or A/B testing of JIT optimizations, routing a small percentage of traffic to the new version while monitoring its performance before full rollout.

### 11.5. Enhanced Workflow Capabilities

*   **Richer Control Flow:** Implementing the advanced control flow steps identified in Section 6 (inspired by n8n [1]): `loop`, `branch`, `merge`, `split`, `wait`, `subworkflow`. This requires significant work in the workflow orchestrator (LLM or JIT runner) and potentially enhancements to the expression language [1].
*   **Sophisticated Error Handling:** Adding configurable, step-level retry policies (with backoff), dead-letter queue mechanisms for persistent failures, and `try/catch/finally`-like blocks within the YAML definition for more granular error management [1].
*   **Richer Expression Language:** Extending the workflow expression syntax beyond basic data access and comparisons to include more built-in functions for string manipulation, array/object processing, date/time functions, mathematical operations, etc., reducing the need for simple transformations to require a dedicated `jit` step [1].
*   **Item Linking / Context Management:** Developing more explicit mechanisms (syntax or dedicated steps) for managing how data items relate across steps, especially within loops or after branching/merging, similar to n8n's item linking concepts [1].

### 11.6. Performance & Scalability

*   **HTTP/2 & HTTP/3 Support:** Upgrading internal (Framework<->Sandbox, MCP) and external HTTP interfaces from HTTP/1.1 to leverage the performance benefits (multiplexing, header compression) of HTTP/2 or the UDP-based advantages of HTTP/3 (QUIC) [1].
*   **Multi-Host Scaling:** Evolving the `SandboxManager` and Core Framework components (`ApplicationRegistry`, `RequestRouter`, etc.) to support clustered deployments across multiple host machines, including mechanisms for inter-host communication, distributed state consistency (if needed beyond Git/Redis), and intelligent cross-host sandbox allocation [1].
*   **Cold Start Mitigation:** Developing strategies to reduce the latency impact of starting new sandbox instances on demand (cold starts), especially if scaling down to zero instances is desired for cost savings [1]. Techniques could include keeping warm standby instances, optimizing container startup times, or using technologies with faster initialization like WASM or pre-initialized microVM snapshots [4].
*   **Resource Management Sophistication:** Implementing more dynamic and fine-grained resource allocation and management for sandboxes via the `SandboxManager`, potentially based on real-time load rather than just static min/max instance counts [1].

### 11.7. Advanced Caching Strategies

*   **Multi-Layer Caching Implementation:** Designing and implementing the multi-layer caching concept mentioned in the UHLP document [1], potentially caching:
    *   Rendered prompts.
    *   LLM completions (based on prompt hash or semantic caching).
    *   JIT code execution results (pure functions).
    *   Final component outputs.
*   **Cache Storage:** Utilizing `StateManagerInterface` runtime state (Redis) [1] or dedicated caching MCP servers (Memcached, Dragonfly).
*   **Cache Invalidation:** Developing robust strategies for cache invalidation, which is notoriously complex, potentially involving TTLs, explicit invalidation calls via MCP, or exploring LLM-driven analysis to determine when cached data becomes stale based on context or state changes [1].

### 11.8. JIT Execution & Reloading Refinements

*   **Server Mode for JIT:** If the V0.1 "Interpreter Mode" proves too slow for high-throughput components, implement an alternative "Server Mode" where JIT code runs within a persistent framework (like FastAPI, Express) inside the sandbox [1, 4].
*   **Hot Reloading (If Server Mode Used):** If "Server Mode" is adopted, re-evaluate the need for and implement a robust `HotReloadManager` mechanism (potentially leveraging framework-specific features or custom signaling) to load new JIT code into the running server processes without requiring container restarts [1].

### 11.9. Framework & MCP API Enhancements

*   **Granular State Reads:** Implementing `StateManagerInterface.GetStateValue` using YAMLPath or JSONPath for more efficient retrieval of specific values from large state files without reading and parsing the entire file [1].
*   **Dynamic MCP Discovery/Registration:** Moving beyond static configuration lookups for MCP server routing towards more dynamic service discovery mechanisms (e.g., Consul, etcd, Kubernetes services) where Community or App-Specific MCP servers can register themselves [1].
*   **Binding Point Specification:** Formally defining the API contract between the Core Framework and the Sandbox internal server beyond the initial HTTP `POST /execute`, potentially exploring alternatives like gRPC or message queues if the request/response pattern proves insufficient for certain interaction types [1].

### 11.10. Tooling & User Experience

*   **Grafana Dashboard Generation:** Implementing the logic (likely LLM-driven via an MCP tool) to automatically generate useful Grafana dashboards based on the metrics exposed by the `MetricCollector` for specific applications [1, 4].
*   **Enhanced Admin Panel:** Adding more sophisticated features to the Admin Panel, such as advanced monitoring views, visual state browsing/editing tools, integrated debugging interfaces, security policy management UIs, and potentially a visual workflow editor.
*   **Improved Testing Framework:** Developing a more comprehensive testing framework for UHLP applications, including automated execution of generated JIT unit tests, integration tests for workflows, and potentially end-to-end testing capabilities.

---

## Glossary

This glossary defines key terms used throughout the UHLP Framework Design Specification.

*   **Admin Panel:** The web-based user interface used by administrators and developers to manage the UHLP framework, applications, configurations, monitoring, and optimization settings.
*   **Application Definition (`AppDefinition`):** The comprehensive definition of a UHLP application, including its ID, metadata, sandbox requirements, state configuration, initial components, security rules, and optimization settings. Stored in the versioned Definition State (Git/YAML).
*   **`ApplicationRegistry`:** The internal Core Framework component responsible for managing the lifecycle, definition, configuration, and security context of all UHLP applications. Provides an internal API for other components.
*   **Binding Point:** The specific mechanism or protocol used for communication between the Core Framework and the internal process within a Sandbox container (V0.1 uses an HTTP `POST /execute` API).
*   **Bootstrap Process:** The process initiated by a user (via the Admin Panel) to define and create a new UHLP application, resulting in the registration of the application, initialization of its state, and provisioning of initial sandbox resources.
*   **Coder LLM:** A Large Language Model specialized or prompted for generating high-quality code (e.g., Python, Node.js) and associated unit tests, used by the `OptimizationOracle`.
*   **`ComponentDefinition`:** An entry within the `ComponentRegistry` defining a specific logical part of an application (e.g., an API endpoint handler, a workflow). Specifies the handler type, target pool, task details, and routing information.
*   **`ComponentRegistry`:** A part of the application's Definition State that maps triggers (like HTTP routes or event names) to specific `ComponentDefinition`s, guiding the `RequestRouter`.
*   **Community MCP Server:** A pluggable, often pre-built, MCP server providing standardized tools for interacting with common external services or databases (e.g., AWS S3, PostgreSQL, Stripe). Scoped per application.
*   **Core Framework:** The stable, foundational software layer of the UHLP system that hosts and orchestrates applications. Includes internal components like `ApplicationRegistry`, `RequestRouter`, `SandboxManager`, etc.
*   **`CoreMCPServer`:** The foundational MCP server, implemented as part of (or closely associated with) the Core Framework. Provides core tools (state access, config, logging, LLM generation, secured command execution) and routes requests to other MCP servers.
*   **Definition State:** The version-controlled state of an application, primarily comprising YAML files and potentially code artifacts stored in a Git repository. Includes `AppDefinition`, `ComponentRegistry`, Workflow YAMLs, Prompt Templates, JIT code. Managed via the `StateManagerInterface`.
*   **Handler Type:** Specifies the execution mechanism for a component (`LLM`, `JIT`, `WORKFLOW`). Determines which kind of sandbox and task details are used.
*   **Hot Reload:** The process of loading updated code (typically JIT code) into a running process or container without requiring a full restart. (Removed for V0.1 JIT Interpreter Mode, potentially relevant for future JIT Server Mode).
*   **Interpreter Mode (JIT V0.1):** The execution model where a JIT sandbox receives a task and invokes the language interpreter directly on the specified script file for each request.
*   **JIT (Just-In-Time) Code:** Code (e.g., Python, Node.js) generated dynamically by the `OptimizationOracle` (using a Coder LLM) to replace performance-critical LLM-based logic.
*   **JIT Runner:** A type of Sandbox container optimized for executing JIT code in a specific language.
*   **LLM (Large Language Model):** The AI model acting as a core part of the runtime, interpreting requests, executing logic based on prompts, or orchestrating workflows.
*   **LLM Orchestrator/Runner:** A type of Sandbox container specialized in interacting with LLMs and potentially orchestrating workflows.
*   **MCP (Model Context Protocol):** The standardized protocol and interface allowing Sandboxed Components to securely request actions and data from the Core Framework or external services via defined "tool calls".
*   **MCP Server:** A server process that implements the MCP protocol and provides specific tools (e.g., `CoreMCPServer`, `AppSpecificMCPServer`, `CommunityMCPServer`).
*   **`MetricCollector`:** The internal Core Framework component responsible for aggregating operational metrics from various sources and exposing them (e.g., via a Prometheus endpoint).
*   **`OptimizationOracle`:** The internal Core Framework component that analyzes metrics, applies configured rules, and orchestrates the generation and deployment of JIT code to optimize application performance or cost.
*   **Pool (Sandbox Pool):** A group of identical Sandbox container instances managed by the `SandboxManager`, typically dedicated to a specific application and functionality (e.g., "App Blog Python JIT Pool").
*   **Prompt Template:** A YAML file defining the structure, metadata, parameters, and template text (using Jinja2) for prompts sent to LLMs. Stored in Definition State.
*   **`RequestRouter`:** The internal Core Framework component that receives incoming requests/events, determines the target component or workflow via the `ApplicationRegistry`, allocates a sandbox via the `SandboxManager`, and dispatches the execution request.
*   **Runtime State:** Ephemeral application state stored in a fast key-value store (Redis for V0.1) used for sessions, temporary workflow data, locks, etc. Managed via the `StateManagerInterface`.
*   **Sandbox / Sandboxed Component:** An isolated execution environment (Docker container for V0.1) where dynamic application logic (LLM interaction, JIT code, workflow orchestration) runs. Managed by the `SandboxManager`.
*   **`SandboxManager`:** The internal Core Framework component responsible for managing the lifecycle (provisioning, monitoring, scaling, termination) of Sandbox containers based on application requirements from the `ApplicationRegistry`.
*   **State:** The collection of data defining an application's configuration, logic, and runtime context. Separated into Definition State (Git/YAML) and Runtime State (Redis).
*   **`StateManagerInterface`:** The internal Core Framework API providing abstracted access to both Definition State (Git/YAML operations) and Runtime State (Redis operations).
*   **UHLP (Ultra High Level Programming):** The programming paradigm where application logic is defined at a very high level (descriptions, prompts, workflows) and executed dynamically, often with an LLM acting as a core part of the runtime.
*   **Workflow Definition:** A declarative YAML file defining a multi-step process involving LLM, JIT, MCP, and control flow steps. Stored in Definition State.
*   **Workflow Orchestrator:** The component (LLM or JIT runner) within a Sandbox responsible for interpreting and executing a Workflow Definition YAML file.

---

## Appendixes

### Appendix A: Example File Structures (Conceptual)

*   **Application State Directory (Git Repository Root):**
    ```
    my-uhlp-app/
    ├── state/
    │   ├── app_definition.yaml       # Main AppDefinition contents
    │   ├── component_registry.yaml   # Component definitions and routes
    │   ├── security_config.yaml      # API keys (hashes), permissions
    │   ├── optimization_config.yaml  # Rules for OptimizationOracle
    │   ├── prompts/                  # Directory for LLM Prompt Templates
    │   │   ├── summarize_data.yaml
    │   │   └── generate_report.yaml
    │   ├── workflows/                # Directory for Workflow Definitions
    │   │   └── process_signup.yaml
    │   ├── schemas/                  # Directory for JSON schemas (e.g., for LLM output)
    │   │   └── signup_payload.schema.json
    │   └── _jit_code/                # Directory for generated JIT code (managed by Oracle)
    │       └── user_validator/
    │           └── v1/
    │               ├── handler.py
    │               └── test_handler.py
    └── .git/                         # Git repository metadata
    ```

### Appendix B: V0.1 Core MCP Tool Summary

A concise list of the primary tools expected to be implemented by the `CoreMCPServer` in the initial version:

*   `core.framework.getConfigValue`
*   `core.framework.logFrameworkMessage`
*   `core.state.getDefinitionFileContent`
*   `core.state.applyDefinitionDiff`
*   `core.state.setDefinitionFileContent` (Use with caution)
*   `core.state.deleteDefinitionFile` (Use with caution)
*   `core.state.listDefinitionDirectory`
*   `core.state.setRuntimeValue`
*   `core.state.getRuntimeValue`
*   `core.state.deleteRuntimeValue`
*   `core.llm.generate`
*   `core.linux.executeCommand` (With strict security implementation)
*   *(Optional V1)* `core.filesystem.readFile`
*   *(Optional V1)* `core.filesystem.writeFile`

### Appendix C: Protobuf Definitions (Partial Index)

*(Note: The full Protobuf messages are defined inline within the relevant component API specifications in Section 3. This appendix serves as an index.)*

*   Messages within `uhlp.framework.ApplicationRegistryService`:
    *   `RegisterApplicationRequest`, `AppDefinition`, `SandboxPoolConfig`, `PoolDefinition`, `ResourceLimits`, `StateConfig`, `ComponentRegistry`, `ComponentDefinition`, `HandlerType`, `RouteMatcher`, `SecurityConfig`, `ApiKeyDefinition`, `InterAppPermission`, `UserRoleDefinition`, `OptimizationConfig`, `OptimizationRule`, `MetricCondition`, `OptimizationAction`
    *   `RegisterApplicationResponse`
    *   `UpdateApplicationRequest`, `AppDefinitionPatch`
    *   `UpdateApplicationResponse`
    *   `DeregisterApplicationRequest`
    *   `DeregisterApplicationResponse`
    *   `GetApplicationStatusRequest`
    *   `GetApplicationStatusResponse`, `AppStatus`
    *   `ListActiveApplicationsRequest`
    *   `ListActiveApplicationsResponse`
    *   `GetApplicationDetailsRequest`
    *   `GetApplicationDetailsResponse`
    *   `GetSandboxRequirementsRequest`
    *   `GetSandboxRequirementsResponse`
    *   `GetComponentDefinitionRequest`, `RouteMatchInput`
    *   `GetComponentDefinitionResponse`
    *   `GetAppConfigurationValueRequest`
    *   `GetAppConfigurationValueResponse` (uses `google.protobuf.Value`)
    *   `ValidateApiKeyRequest`
    *   `ValidateApiKeyResponse`
    *   `GetApplicationPermissionsRequest`
    *   `GetApplicationPermissionsResponse`
    *   `GetUserPermissionsForAppRequest`
    *   `GetUserPermissionsForAppResponse`
*   Messages within `uhlp.framework.StateManagerService`:
    *   `GetDefinitionFileContentRequest`, `GetDefinitionFileContentResponse`
    *   `ApplyDefinitionDiffRequest`, `ApplyDefinitionDiffResponse`
    *   `SetDefinitionFileContentRequest`, `SetDefinitionFileContentResponse`
    *   `DeleteDefinitionFileRequest`, `DeleteDefinitionFileResponse`
    *   `ListDefinitionDirectoryRequest`, `ListDefinitionDirectoryResponse`, `DirectoryEntry`, `EntryType`
    *   `SetRuntimeValueRequest` (uses `google.protobuf.Value`), `SetRuntimeValueResponse`
    *   `GetRuntimeValueRequest`, `GetRuntimeValueResponse` (uses `google.protobuf.Value`)
    *   `DeleteRuntimeValueRequest`, `DeleteRuntimeValueResponse`
*   Messages within `uhlp.framework.SandboxManager` Allocation API (Conceptual):
    *   `AllocateSandboxRequest`, `AllocateSandboxResponse`, `AllocationStatus`
    *   `ReleaseSandboxRequest`
*   Messages within `uhlp.framework.MetricCollector` Input API (Conceptual - OTLP Inspired):
    *   `RecordMetricsRequest`, `Metric`, `Gauge`, `Sum`, `Histogram`, `AggregationTemporality`, `NumberDataPoint`, `HistogramDataPoint`

### Appendix D: Open Questions / V2+ Areas

*(This appendix reiterates key areas identified in Section 11 that require further design or are deferred to future versions)*

*   Advanced State Consistency mechanisms beyond Git locking + Redis atomics.
*   Enhanced Debugging & Observability tooling (visual tracing, time-travel, etc.).
*   Security enhancements (stricter sandboxing via Firecracker, LLM Security focus, Formal Verification).
*   Advanced Optimization Logic (ML-driven Oracle, Dynamic Rollback, A/B testing).
*   Enhanced Workflow Capabilities (Looping, Branching, Merging, Splitting, Waiting, Subworkflows, Advanced Error Handling, Richer Expressions).
*   Performance & Scalability improvements (HTTP/2/3, Multi-Host Scaling, Cold Start Mitigation).
*   Advanced Caching Strategies (Multi-layer, sophisticated invalidation).
*   JIT Server Mode execution and potential Hot Reloading.
*   Framework & MCP API enhancements (granular state reads, dynamic MCP discovery).
*   Enhanced Tooling & User Experience (Grafana generation, Advanced Admin Panel, Testing Framework).
```

---

This concludes the generation of the comprehensive UHLP Framework Design Specification document based on our extensive collaboration. Please review it carefully. This document should provide a detailed blueprint suitable for guiding the implementation phase, including generating prompts for an LLM coder. Let me know if you have any adjustments or further questions!