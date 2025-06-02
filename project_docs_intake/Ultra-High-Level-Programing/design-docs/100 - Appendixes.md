## ## Appendixes

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

*(Note: The full Protobuf messages are defined inline within the relevant component API specifications in Section 3. This appendix could list the main message names for quick reference if desired, or contain the full combined .proto file content if generated separately).*

*   `AppDefinition`, `SandboxPoolConfig`, `ComponentDefinition`, `SecurityConfig`, etc. (within `ApplicationRegistryService`)
*   `RecordMetricsRequest`, `Metric`, `NumberDataPoint`, `HistogramDataPoint` (within `MetricCollector`)
*   Requests/Responses for `StateManagerService` methods (e.g., `GetDefinitionFileContentRequest`, `ApplyDefinitionDiffRequest`, `SetRuntimeValueRequest`)
*   Requests/Responses for `SandboxManager` allocation API (`AllocateSandboxRequest`, `AllocateSandboxResponse`)

### Appendix D: Open Questions / V2+ Areas

*(This appendix can reiterate the key areas identified in Section 11 that require further design or are deferred to future versions, such as advanced workflow logic, robust state consistency, sophisticated optimization/rollback, enhanced security models, multi-host scaling, etc.)*