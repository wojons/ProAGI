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