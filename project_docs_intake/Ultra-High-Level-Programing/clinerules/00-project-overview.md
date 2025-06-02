# UHLP Project Overview & Core Principles (`00-project-overview.md`)

## Project Goal

The primary goal of the UHLP (Ultra High Level Programming) project is to design and build a framework and runtime environment where applications are defined using high-level, human-readable descriptions (primarily natural language and structured configuration), and where a Large Language Model (LLM) **acts as the core dynamic runtime logic engine**.

**Key Objective:** Empower users/developers (potentially less technical ones) to create and deploy complex, interactive applications by describing *what* the application should do, rather than writing low-level imperative code. Bridge the gap between natural language intent and functional software.

## Core Concepts

1.  **LLM as Runtime:** The central principle is that the LLM isn't just a code generator; it *is* the dynamic logic engine for significant parts of the application, interpreting requests and orchestrating actions based on the defined state and workflow [1].
2.  **Ultra High-Level Abstraction:** UHLP sits above traditional VHLLs (like Python/JS). The LLM acts as the next-level abstraction layer, managing complex logic, state, and interactions based on high-level user intent [1].
3.  **Declarative Definition:** Applications are primarily defined through declarative means: natural language descriptions, structured YAML configuration files (for state, components, workflows, prompts), and potentially graphical interfaces (via an Admin Panel) [1].
4.  **State-Driven Behavior:** The application's structure, logic flow, prompts, component mappings, and optimization rules are stored in a version-controlled state repository (Git+YAML primarily for definitions, Redis for runtime state) [1]. The framework and LLM runtime interpret this state to determine behavior.
5.  **Adaptive Runtime (JIT):** The system is dynamic and adaptive [1]:
    *   **Predictive:** Sets up initial templates/prompts based on the application definition.
    *   **Reactive:** Generates or refines components (prompts, code) during runtime based on requests.
    *   **Optimizing:** Monitors performance/cost and can choose to replace LLM-interpreted logic with JIT-generated, persistent code (e.g., Python, Node.js) for efficiency, based on configurable rules [1].
6.  **Sandboxed Execution:** Dynamic components (LLM interactions, JIT code) run within isolated Docker containers (Sandboxes) managed by the Core Framework [1]. Interaction occurs via specified APIs (e.g., `/execute` endpoint).
7.  **Model Context Protocol (MCP):** A standardized interface (`core.*`, `community.*`, `app.*` tools) for Sandboxes to interact securely and consistently with the framework, external services, databases, filesystem, Linux commands, and other resources [1].

## Target Persona (Developer/User)

*   **Initial Target:** Developers or technically-inclined users comfortable with defining application logic through structured configuration (YAML), writing prompts, and potentially reviewing/guiding JIT code generation.
*   **Long-Term Vision:** Enable less technical users ("creators") to build applications primarily through natural language descriptions and interactive configuration, similar to platforms like Roblox [1].

## Guiding Principles for Development

*   **Modularity:** Design components (Core Framework modules, MCP servers, Sandboxes) with clear interfaces and separation of concerns.
*   **Declarative Approach:** Favor defining behavior declaratively in state (YAML) over hardcoding logic in the framework whenever possible.
*   **Extensibility:** Build the framework (especially MCP, Workflow engine) to be extensible.
*   **Security:** Embed security considerations from the start (sandboxing, scoped tool access, input validation, permissions).
*   **Testability:** Ensure components are testable, including generated JIT code (LLM should generate tests alongside code) [1].
*   **Iterative Development:** Start with a core V0/V1 and iteratively add advanced features (complex workflow logic, sophisticated optimization, multi-host scaling).

**(Self-Correction Note for AI Assistant):** Always refer back to the detailed UHLP Design Specification document when implementing features. Ground decisions in the defined architecture (API contracts, component responsibilities, state structure). Avoid introducing concepts from unrelated projects (like 'xAIx'). Focus on implementing the UHLP vision as specified.