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