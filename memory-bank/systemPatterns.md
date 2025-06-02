# System Patterns

## System Architecture
Nexus CoCreate AI is architected based on the principles and components of the Ultra High Level Programming (UHLP) framework to support the creation, deployment, and management of AI agents and applications. The architecture is designed around a stable Core Framework that orchestrates dynamic components running in isolated Sandboxes, interacting via the Model Context Protocol (MCP).

The key components and their roles are:

1.  **Core Framework:** The stable, foundational layer responsible for orchestrating application execution (Section 02.0, 02.1). It includes internal components like:
    *   **ApplicationRegistry:** Manages application definitions, configuration, and security context (Section 03.1, 02.1.1).
    *   **RequestRouter:** Ingests requests/events, identifies the target component/workflow, allocates sandboxes, and dispatches execution requests (Section 03.4, 03.14).
    *   **SandboxManager:** Manages the lifecycle (provisioning, monitoring, scaling) of Sandbox containers (Docker in V0.1) (Section 03.2, 02.1.2).
    *   **StateManagerInterface:** Provides abstracted access to application state (Definition/Config in Git/YAML, Runtime in Redis) (Section 03.3, 02.1.3, 03.15).
    *   **ToolManager:** Discovers, registers, and executes tools (core and MCP) (Section 03.7, 03.11).
    *   **McpHub:** Manages connections to external MCP servers and exposes their tools/resources (Section 03.8).
    *   **EventBus:** Handles asynchronous communication and event distribution (Section 03.9, 03.12).
    *   **LoggingService:** Collects, processes, and stores structured logs (Section 03.10, 04.6).
    *   **OptimizationOracle:** Analyzes metrics and orchestrates JIT compilation (Section 02.1.6).

2.  **Sandboxed Components:** Isolated execution environments (Docker containers for V0.1) where dynamic application logic runs (Section 02.0, 02.1). Types include:
    *   **JIT Runner:** Executes JIT-generated code (Section 02.1.5).
    *   **LLM Orchestrator/Runner:** Interacts with LLMs and orchestrates workflows (Section 02.1.5).
    *   **AI Logic:** Represents the core AI capabilities and reasoning engine within a Sandbox (Section 03.18).

3.  **Model Context Protocol (MCP) Servers:** Provide standardized interfaces for Sandboxed Components to interact with capabilities and external services (Section 03.8).
    *   **CoreMCPServer:** Implements foundational framework tools and routes requests (Section 03.8.5).
    *   **AppSpecificMCPServer:** (Per-application) Implements custom application tools and routes requests (Section 03.8.3).
    *   **CommunityMCPServer:** (Pluggable) Provides tools for common external services (databases, APIs) (Section 03.8.3).

4.  **Application State:**
    *   **Definition/Config State:** Version-controlled (Git/YAML) storage for application definitions, component registries, workflows, prompts, and JIT code (Section 03.3.1, 03.15).
    *   **Runtime State:** Ephemeral key-value store (Redis) for session data, temporary workflow state, etc. (Section 03.3.2, 03.15).
    *   **Application Domain Data:** External databases accessed via Community MCPs (Section 03.3.3).
    *   **Agent/Application Context & Memory:** Dedicated store for each agent/app, part of Definition State (Section 03.21).

5.  **Frontend (Admin Panel / User UI):** A web interface for users to interact with the platform, manage applications, define logic (via workflows/prompts), monitor performance, and configure settings (Section 03.20). This UI interacts with the Core Framework's internal APIs.

6.  **Deployment Infrastructure:** Mechanisms for packaging and deploying the Core Framework and MCP servers (e.g., Docker Compose for self-hosting) (Section 07.0).

## Key Technical Decisions
- Build a Proof of Concept (POC) focusing on core functionality and self-hosting (Section 01.0, 07.0).
- Prioritize core functionality over advanced security for the initial POC (while integrating security principles from the UHLP design) (Section 06.0).
- **Adopt the UHLP Framework Architecture:** Base the Nexus CoCreate AI technical implementation on the UHLP design specification (Section 02.0, 02.1).
- **State Management:** Use Git/YAML for versioned Definition/Config state and Redis for Runtime state, accessed via the StateManagerInterface (Section 03.3, 03.15).
- **Sandboxing:** Utilize Docker containers for Sandboxed Components in V0.1 (acknowledging limitations and considering future alternatives like Firecracker) (Section 03.2, 06.1).
- **Tooling & Integrations:** Standardize all interactions with framework capabilities and external services via the Model Context Protocol (MCP) using Core, App-Specific, and Community servers (Section 03.8).
- **Application Logic Definition:** Use declarative Workflow YAML for orchestrating multi-step logic and LLM Prompt Template YAML for defining LLM interactions (Section 04.0, 03.18.1).
- **Adaptive Runtime:** Implement the JIT optimization process orchestrated by the OptimizationOracle to dynamically replace LLM logic with generated code based on metrics (Section 02.1.6).
- **API Key Management:** Implement secure storage (hashing, secrets management) and validation of API keys via the ApplicationRegistry and SecurityConfig (Section 06.3).
- **Containerization:** Use Docker for packaging and deployment (Section 07.0).
- Use Python for the Core Framework implementation (Section 07.0).
- Implement a web-based user interface (Admin Panel) interacting with framework APIs (Section 03.20).
- Support for self-hosting deployment (e.g., Docker Compose) (Section 07.0).
- Agent/Application templating system (aligned with UHLP AppDefinition and state structure) (Section 03.16).
- Per-agent/application Context & Memory for context persistence (integrated with UHLP state management or via a dedicated MCP) (Section 03.21).
- Scalability, multi-tenancy, self-correction, learning mechanisms (future considerations, aligned with UHLP V2+) (Section 08.0).

## Design Patterns (Integrated from UHLP)
- **Orchestration:** The Core Framework orchestrates Sandboxes and MCP interactions (Section 02.0).
- **Gateway/Proxy:** MCP servers act as gateways for controlled access (Section 03.8).
- **Observer Pattern:** MetricCollector gathers data from various sources (Section 02.1.7).
- **Strategy Pattern:** RequestRouter selects execution paths (LLM/JIT) (Section 03.14).
- **Repository Pattern:** StateManagerInterface abstracts state access (Section 03.3).
- **Factory Pattern:** SandboxManager provisions container instances (Section 03.2).
- **Declarative Configuration:** Application logic defined in YAML (Workflows, Prompts) (Section 04.0, 03.18.1).
- **Adaptive/JIT Compilation:** OptimizationOracle dynamically replaces logic (Section 02.1.6).

## Component Relationships
```mermaid
graph TD
    User --> AdminPanel[Admin Panel / User UI]
    AdminPanel <--> CoreFramework[Core Framework]

    CoreFramework --> ApplicationRegistry[Application Registry]
    CoreFramework --> RequestRouter[Request Router]
    CoreFramework --> SandboxManager[Sandbox Manager]
    CoreFramework --> StateManagerInterface[State Manager Interface]
    CoreFramework --> MetricCollector[Metric Collector]
    CoreFramework --> OptimizationOracle[Optimization Oracle]
    CoreFramework --> ToolManager[Tool Manager]
    CoreFramework --> McpHub[MCP Hub]
    CoreFramework --> EventBus[Event Bus]
    CoreFramework --> LoggingService[Logging Service]


    RequestRouter --> SandboxManager
    RequestRouter --> Sandboxes[Sandboxed Components (Docker)]
    SandboxManager --> Sandboxes
    Sandboxes --> CoreFrameworkAPI[Core Framework API]
    CoreFrameworkAPI --> StateManagerInterface
    CoreFrameworkAPI --> ToolManager
    CoreFrameworkAPI --> LoggingService
    CoreFrameworkAPI --> EventBus
    CoreFrameworkAPI --> ApplicationRegistry

    ToolManager --> McpHub
    McpHub --> MCPServers[MCP Servers (Core/App/Community)]
    MCPServers --> ExternalServices[External Services (LLMs, Databases, Tools)]

    StateManagerInterface --> DefinitionState[Definition State (Git/YAML)]
    StateManagerInterface --> RuntimeState[Runtime State (Redis)]
    ExternalServices --> ApplicationDomainData[Application Domain Data (External DBs)]

    MetricCollector --> OptimizationOracle
    Sandboxes --> MetricCollector

    EventBus --> AdminPanel
    EventBus --> LoggingService
    EventBus --> OtherSubscribers[Other Subscribers]

    LoggingService --> LogStorage[Log Storage/Monitoring]

    subgraph Nexus CoCreate AI Architecture
        CoreFramework
        Sandboxes
        MCPServers
        DefinitionState
        RuntimeState
        ApplicationDomainData
        CoreFrameworkAPI
        LogStorage
        OtherSubscribers
    end

    subgraph External World
        User
        ExternalServices
    end

    classDef default fill:#f9f,stroke:#333,stroke-width:2px;
    classDef core fill:#ccf,stroke:#333,stroke-width:2px;
    classDef external fill:#cfc,stroke:#333,stroke-width:2px;

    class ApplicationRegistry,RequestRouter,SandboxManager,StateManagerInterface,MetricCollector,OptimizationOracle,ToolManager,McpHub,EventBus,LoggingService core;
    class AdminPanel,MCPServers,DefinitionState,RuntimeState,ApplicationDomainData,ExternalServices,User,CoreFrameworkAPI,LogStorage,OtherSubscribers external;

```

## Critical Implementation Paths
- **Core Framework Components:** Implementing the ApplicationRegistry, RequestRouter, SandboxManager, StateManagerInterface, MetricCollector, OptimizationOracle, ToolManager, McpHub, EventBus, and LoggingService (Section 02.1, 03.1-03.10, 03.17-03.23).
- **Sandbox Execution:** Building the base sandbox images and the internal `/execute` API handler (Section 03.2, 03.5).
- **Model Context Protocol (MCP):** Implementing the CoreMCPServer and defining/integrating key Community MCP tools (Section 03.8).
- **State Management:** Setting up the Git/YAML and Redis state stores and ensuring the StateManagerInterface works correctly (Section 03.3, 03.15).
- **Workflow & Prompt Execution:** Implementing the workflow orchestration logic within a sandbox and the prompt rendering/LLM invocation flow (Section 04.0, 03.18.1).
- **Secure API Key Management:** Implementing secure storage and validation mechanisms (Section 06.3).
- **Admin Panel:** Building the initial UI for application management and configuration (Section 03.20).
- **Self-hosting Deployment:** Creating Docker Compose or similar configurations for easy setup (Section 07.0).
- **JIT Optimization Flow:** Implementing the Oracle's logic and the code generation/activation process (Section 02.1.6).
