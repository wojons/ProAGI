# State Management Guidelines (`03-state-management.md`)

This document defines the rules and best practices for managing and accessing application state within the UHLP framework. Consistent state management is critical for application behavior, versioning, and observability.

## 1. State Storage Mechanisms

*   **Definition/Configuration State:**
    *   **Primary Storage:** Version-controlled repository (managed by **Git**) containing **YAML files**. This is the source of truth for application structure, component configurations, workflow definitions, prompt templates, and optimization rules [1].
    *   **Location:** Stored within the application-specific state directory (e.g., `UHLP_Runtime/state/<appId>/`).
    *   **Benefits:** Versioning, traceability, auditability, LLM processability [1].
*   **Runtime/Ephemeral State:**
    *   **Primary Storage:** Key-value store (default: **Redis**) accessible via the framework [1].
    *   **Purpose:** Used for temporary data required during request processing, session information, distributed locks, short-lived caches, or intermediate workflow state [1].
*   **Application Domain Data:**
    *   **Storage:** Use external databases (e.g., PostgreSQL, MongoDB via Supabase) or other appropriate storage solutions.
    *   **Access:** Accessed **exclusively** via **Community or Application-Specific MCP servers**, *not* directly managed by the framework's `StateManagerInterface` [1].

## 2. State Access Control

*   **Exclusive Access via `StateManagerInterface`:** All interactions (read/write) with both Definition/Config State (Git/YAML) and Runtime State (Redis) **MUST** go through the **`StateManagerInterface`** internal framework API [1].
*   **MCP Wrappers:** Sandboxes (JIT/LLM) access state **only** through the corresponding **Core MCP tool wrappers** (e.g., `core.state.getDefinitionFileContent`, `core.state.setRuntimeValue`) [1]. Direct access to underlying Git repositories or Redis instances from sandboxes or other framework components is strictly prohibited.
*   **Scope:** All state access operations via the interface are implicitly scoped by `appId` [1].

## 3. Modifying Definition/Configuration State (Git/YAML)

*   **Primary Method: `ApplyDefinitionDiff`:** Modifications to existing YAML files **SHOULD** predominantly use the `StateManagerInterface.ApplyDefinitionDiff` method (or its `core.state.applyDefinitionDiff` MCP wrapper) [1].
    *   This ensures changes are applied as patches, leveraging Git for merging and conflict detection.
    *   It preserves history more granularly.
*   **Use `SetDefinitionFileContent` Sparingly:** Only use `SetDefinitionFileContent` when creating entirely new files or when a complete overwrite is explicitly intended and justified [1]. Exercise caution as it bypasses diff-based merging.
*   **Optimistic Concurrency:** Always provide the `expectedBaseRevision` when calling `ApplyDefinitionDiff` to prevent accidentally overwriting concurrent changes [1]. Handle potential conflicts reported by the interface gracefully (e.g., by retrying with a fresh read and re-generating the diff).
*   **Git Commit Messages:** Calls to `ApplyDefinitionDiff`, `SetDefinitionFileContent`, or `DeleteDefinitionFile` require a meaningful `commitMessage`. This message **MUST** be clear, concise, and ideally reference the context or reason for the change (e.g., "Optimize component X to JIT via OptimizationOracle rule R1", "Update workflow Y based on user request #123") [1].

## 4. YAML File Structure & Content

*   **Clarity & Readability:** Write clean, well-formatted YAML. Use consistent indentation (2 spaces recommended).
*   **Comments:** Use comments (`#`) liberally to explain the purpose of non-obvious configurations, sections, or specific values.
*   **Modularity:** Break down large configurations into logical smaller files where appropriate (e.g., separate files for workflows, prompt templates, component definitions). Use clear naming conventions for files and directories [1].
*   **Schema Adherence:** Where applicable (e.g., Workflow YAML, Prompt Templates), ensure the structure strictly adheres to the defined specifications.
*   **Avoid Redundancy:** Define common values or configurations centrally (e.g., in `ApplicationDefinition`) and reference them where needed, rather than duplicating them.

## 5. Runtime State (Redis) Usage

*   **Ephemeral Data Only:** Use runtime state only for data that does not need to be permanently persisted or versioned (e.g., session IDs, task locks, intermediate workflow results, short-term caches) [1].
*   **Keys:** Use clear, namespaced keys (e.g., `lock:workflow:<workflow_instance_id>`, `session:<session_id>`). Include `appId` implicitly or explicitly in the key structure if the underlying Redis instance is shared.
*   **TTLs:** Set appropriate Time-To-Live (TTL) values for runtime state keys to ensure automatic cleanup of stale data [1]. Avoid creating keys that live forever unless absolutely necessary and managed explicitly.

## 6. Security Considerations

*   **No Secrets in State:** **DO NOT** store sensitive data (API keys, passwords, database credentials, encryption keys, PII) directly within the Git/YAML state files. Use environment variables injected into the framework/sandboxes, a dedicated secrets management system accessed via framework configuration, or specifically designed secure MCP tools.
*   **Access Control:** State access via the `StateManagerInterface` and MCP wrappers must be subject to the framework's overall authorization controls (ensuring App A cannot modify App B's state).

## 7. Backup & Recovery

*   **Git as Primary Backup:** The inherent nature of using Git provides the primary backup and history for the Definition/Configuration state [1]. Regular Git repository backups (e.g., cloning the repository) are recommended.
*   **Runtime State Backup (Optional):** Backups for Runtime State (Redis) depend on the persistence configuration of the Redis instance and the criticality of the ephemeral data. Standard Redis backup procedures can be used if needed.
*   **Upgrade Process:** Major upgrades involving state structure changes may involve: exporting relevant state (potentially via `GetDefinitionFileContent`), processing/transforming files (possibly using an LLM), and re-importing/applying changes via `ApplyDefinitionDiff` or `SetDefinitionFileContent` [1].
