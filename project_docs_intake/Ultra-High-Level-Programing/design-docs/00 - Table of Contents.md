# UHLP (Ultra High Level Programming) Framework Design Specification (V0.1)

## 1. Concept Overview (Reference: UHLP Document Section I)
    1.1. Core Idea: LLM as Runtime
    1.2. Abstraction Layer
    1.3. User Experience Analogy (Roblox-like)
    1.4. JIT / Adaptive Nature (Predictive, Reactive, Optimizing)

## 2. Core Architecture (Reference: UHLP Document Section II)
    2.1. Immutable Core Framework Overview
    2.2. Sandboxed Components Overview (Docker Containers)
        2.2.1. Sandbox Types (JIT Runner, LLM Orchestrator/Runner)
        2.2.2. Execution Model (V0.1: Interpreter Mode for JIT)
    2.3. Interaction Model (Request Flow)
    2.4. **Core Framework -> Sandbox API Specification**
        2.4.1. Endpoint: `POST /execute`
        2.4.2. Transport & Hosting
        2.4.3. Request Structure (Headers, Body: `requestId`, `requestData`, `context`)
        2.4.4. Response Structure (HTTP Statuses, Body: `requestId`, `resultType`, `data`, `metrics`)

## 3. Core Framework Internal Components & APIs
    3.1. **`ApplicationRegistry` Internal API Specification**
        3.1.1. Purpose & Transport (gRPC)
        3.1.2. Methods (Register/Update/Deregister/Status/List Applications)
        3.1.3. Methods (Get Details, Get Sandbox Requirements, Get Component Definition, Get Config)
        3.1.4. Methods (Security: ValidateApiKey, Get Permissions)
        3.1.5. Core Data Structures (`AppDefinition`, `SandboxPoolConfig`, `ComponentDefinition`, etc.)
    3.2. **`SandboxManager` Specification**
        3.2.1. Purpose & Responsibilities
        3.2.2. Discovery (Via `ApplicationRegistry` API)
        3.2.3. Docker Resource Management (via Docker Socket)
        3.2.4. Pool Management (Per-Application Pools)
        3.2.5. Health Monitoring & Recycling (Basic)
        3.2.6. Instance Allocation API (`AllocateSandbox`/`ReleaseSandbox`)
    3.3. **`StateManagerInterface` Internal API Specification**
        3.3.1. Purpose & Transport (gRPC)
        3.3.2. State Scopes (Definition/Config vs. Runtime)
        3.3.3. Definition State Methods (Git/YAML: Get/ApplyDiff/Set/Delete/List File Content)
        3.3.4. Runtime State Methods (Redis: Set/Get/Delete Runtime Value)
    3.4. **`RequestRouter` Specification**
        3.4.1. Purpose & Hosting
        3.4.2. Input & Core Logic Flow
        3.4.3. Component/Workflow Identification (Via `ApplicationRegistry`)
        3.4.4. Sandbox Allocation (Via `SandboxManager`)
        3.4.5. `/execute` Request Construction (Handling Workflow vs. Direct Call)
        3.4.6. Sandbox Response Handling & Final Response Generation
    3.5. **`MetricCollector` Specification**
        3.5.1. Purpose & Hosting
        3.5.2. Input Interface (Push API - OTLP Inspired)
        3.5.3. Key Attributes/Labels (`appId`, `componentId`, etc.)
        3.5.4. Output Interface (Prometheus Exposition Format via `GET /metrics`)
        3.5.5. Extensibility (Handling Custom Metrics)
    3.6. **`OptimizationOracle` Specification (V0.2 - Enhanced Control)**
        3.6.1. Purpose & Hosting
        3.6.2. Data Acquisition (Via `MetricCollector`)
        3.6.3. Decision Trigger (Rule-Based via Admin Panel Config: Global/App/Component)
        3.6.4. Manual Trigger Support
        3.6.5. JIT Process Initiation (Spec Generation, Coder LLM Invocation, Artifact Storage via `StateManager`)
        3.6.6. Triggering State Update (No HotReloadManager needed for V0.1)

## 4. State Management Details (Reference: UHLP Document Section III)
    4.1. Conceptual Content (`ApplicationDefinition`, `ComponentRegistry`, `RuntimeData`, etc.)
    4.2. Storage Mechanisms
        4.2.1. Definition/Config: Git + YAML Files (Primary Source of Truth)
        4.2.2. Runtime Ephemeral State: Redis
        4.2.3. Application Domain Data: External Databases (via MCP)
    4.3. Access API (Provided by `StateManagerInterface`)

## 5. Model Context Protocol (MCP) (Reference: UHLP Document Section IV)
    5.1. Role & Purpose
    5.2. Multi-Server Architecture (Core, App-Specific, Community)
    5.3. Scoping (Core=Shared, App/Community=Per-Application)
    5.4. **`CoreMCPServer` Specification**
        5.4.1. Purpose, Hosting (Separate Container), Transport (HTTP)
        5.4.2. Authentication/Authorization (Per-App Context)
        5.4.3. Routing Logic (Core vs. Downstream)
        5.4.4. V1 Core Toolset Implementation Details:
            5.4.4.1. `core.framework.*` (getConfigValue, logFrameworkMessage)
            5.4.4.2. `core.state.*` (Wrappers for `StateManagerInterface`)
            5.4.4.3. `core.llm.generate` (Standardized LLM Invocation)
            5.4.4.4. `core.linux.executeCommand` (Detailed Security Implementation: Whitelist, Wrappers)
            5.4.4.5. `core.filesystem.*` (Scoped File Access - Optional V1)

## 6. Workflow Definition
    6.1. **Workflow YAML Structure Specification**
        6.1.1. Purpose & File Location
        6.1.2. Top-Level Properties (`workflowId`, `trigger`, `startAt`, `steps`)
        6.1.3. Step Definition (`stepId`, `type`, `target`, `inputMapping`, `transitions`)
        6.1.4. Step Types (`jit`, `llm`, `mcp`, `control` - incl. `formatResponse`)
        6.1.5. Expression Syntax (Dot Notation, Literals, Basic Logic)
        6.1.6. Transitions & Flow Control (`onSuccess`, `onFailure`, `condition`, `end`)
    6.2. Enhancements Inspired by n8n (Loops, Merging, Error Handling - Placeholders for V2)

## 7. Dynamic Execution & Optimization (Reference: UHLP Document Section V)
    7.1. Runtime Decision Making (Handled by `OptimizationOracle`)
    7.2. Execution Paths (LLM vs. JIT)
    7.3. JIT Code Generation Workflow (Detailed within `OptimizationOracle`)
    7.4. Multi-Layer Caching (Concept - Not Specified in Detail for V1)

## 8. Prompt Template Format
    8.1. **LLM Prompt Template Format Specification**
        8.1.1. Purpose & File Format (YAML)
        8.1.2. Structure (Metadata + `template`)
        8.1.3. Templating Engine (Jinja2)
        8.1.4. Output Specification (`outputFormat`, `outputSchema`)

## 9. UI & Application Lifecycle (Reference: UHLP Document Section VI & VII)
    9.1. UI Generation (LLM generated HTML/CSS/JS - Served by Core Framework)
    9.2. Bootstrap Process (User defines app via Admin Panel -> `ApplicationRegistry.RegisterApplication`)
    9.3. Deployment (Shareable subdomain, Access Control Flags - Managed by Framework)
    9.4. Admin Panel Requirements (V1 Sketch: App Management, Status, Opt-Rule Config)

## 10. Security Considerations (Integrated & Future Work)
    10.1. Sandbox Isolation (Docker Dependency Isolation)
    10.2. Secured Command Execution (`core.linux.executeCommand`)
    10.3. API Key Management (`ApplicationRegistry`, Validation)
    10.4. Inter-App Communication Permissions (Framework Rules Needed)
    10.5. MCP Scoping & Permissions (App Context Enforcement)
    10.6. State Access Control (Via `StateManagerInterface`)

## 11. Future Work / V2+ Considerations
    11.1. Advanced Optimization Logic (ML Models, Dynamic Rollback)
    11.2. Enhanced Workflow Capabilities (Looping, Merging, Subworkflows, Waiting, Error Handling)
    11.3. HTTP/2 & HTTP/3 Support
    11.4. Multi-Host Scaling (`SandboxManager`, Framework Clustering)
    11.5. Grafana Dashboard Generation
    11.6. Advanced Caching Strategies
    11.7. More Sophisticated JIT Execution Modes (Server Mode, Hot Reloading if needed)
    11.8. Debugging/Observability Tooling for UHLP flows