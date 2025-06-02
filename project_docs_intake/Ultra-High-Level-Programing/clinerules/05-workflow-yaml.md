# Workflow YAML Standards (`05-workflow-yaml.md`)

This document outlines the standards and best practices for creating Workflow YAML definition files (e.g., `workflows/my_workflow.yaml`) within UHLP applications. These workflows orchestrate the application's logic by defining sequences of JIT, LLM, and MCP steps [1, 4].

## 1. File Structure & Metadata

*   **File Location:** Store workflow definitions within the application's state directory, typically under `workflows/` [1]. Use descriptive filenames (e.g., `user_authentication.yaml`).
*   **Required Fields:** Every workflow file **MUST** include:
    *   `workflowId`: A unique, versioned identifier for the workflow (e.g., `user_auth_v1`).
    *   `startAt`: The `stepId` of the initial step to execute [1].
    *   `steps`: A map containing all step definitions [1].
*   **Optional Metadata:** Include `description` to clarify the workflow's purpose. Define `trigger` information clearly [1].

## 2. Step Definitions (`steps:`)

*   **Unique `stepId`:** Each step within the `steps` map **MUST** have a unique key (`stepId`) that is descriptive (e.g., `validate_user_input`, `fetch_product_details`) [1].
*   **`type` Specification:** Clearly specify the step `type`: `jit`, `llm`, `mcp`, or `control` [1].
*   **`description`:** Provide a concise `description` for each step explaining its purpose.
*   **`target` Definition:** Define the `target` appropriately based on the step `type`:
    *   `jit`: Include `language`, `script` path (relative to app state root), and `function` name [1].
    *   `llm`: Include `promptTemplate` path or inline `prompt`. Optionally include `model` override [1].
    *   `mcp`: Include the full `tool` name (e.g., `core.state.getFileContent`) [1].
    *   `control`: Include `subtype` if applicable (e.g., `formatResponse`).

## 3. Data Mapping (`inputMapping`)

*   **Clarity:** Use the defined Expression Syntax clearly and consistently to map required inputs for each step [1].
*   **Source Data:** Reference data primarily from `trigger.*`, `steps.<stepId>.output.*`, or `context.*` [1].
*   **Avoid Complex Logic:** Keep mappings focused on data selection and simple transformations (if supported by expression functions). **DO NOT** embed complex business logic directly within `inputMapping`. Use dedicated `jit` or `control` steps for complex data preparation or transformations.
*   **Quoting Literals:** Remember to use single quotes for string literals (e.g., `query: "'SELECT * ...'"`).

## 4. Flow Control (`transitions`)

*   **Explicit Termination:** All logical paths through the workflow **MUST** eventually reach a step with `transitions: end: true` [1]. Ensure there are no infinite loops or dead ends without explicit termination.
*   **Clear Conditions:** When using conditional transitions (`condition:`), the expression **MUST** evaluate to a boolean (`true`/`false`) [1]. Use the expression syntax clearly. Keep conditions understandable.
*   **Default Paths:** Provide default transition paths (`onSuccess`, `onFailureDefault`, or a transition without a `condition`) to handle expected outcomes and general failures gracefully [1].
*   **Readability:** Order transitions logically. Use comments if the flow logic is complex.

## 5. Expression Syntax Usage

*   **Consistency:** Use the defined dot notation consistently for accessing data [1].
*   **Simplicity (V1):** Favor simple data access paths. Rely on standard comparison operators (`==`, `!=`, `>`, etc.) and logical operators (`&&`, `||`, `!`) for conditions [1]. (Avoid overly complex chained function calls if/when expression functions are added).
*   **Error Handling:** Be mindful that accessing non-existent paths (e.g., `steps.previous.output.non_existent_field`) might result in errors or null values depending on the interpreter implementation. Access optional data defensively (perhaps using `defined()` if added to syntax).

## 6. Control Steps (`type: control`)

*   **`formatResponse`:** Use the `formatResponse` subtype exclusively for preparing the final output structure of the workflow intended to be returned to the caller (Core Framework) [1]. Set `resultType` and `data` appropriately according to the Workflow Specification [1]. Remember to include `transitions: end: true`.
*   **(Future Logic):** While V1 focuses on `formatResponse`, anticipate future `control` subtypes like `loop`, `branch`, `wait`, `map`, `merge` [1]. Structure workflows logically now to accommodate these later without major refactoring where possible (e.g., using distinct steps for data preparation vs. external calls).

## 7. Error Handling Practices

*   **Anticipate Failures:** Consider potential failure points for `jit`, `llm`, and `mcp` steps (e.g., validation errors, external service unavailability, LLM errors, database errors).
*   **Graceful Handling:** Use `onFailure`, `onFailureDefault`, or conditional failure transitions to route execution to appropriate error-handling steps (e.g., steps that log the error and use `formatResponse` with `resultType: 'error'`) [1].
*   **Specificity:** Catch specific anticipated errors using conditional `onFailure` transitions where possible (e.g., branching based on `step.output.error.code`) [1]. Use `onFailureDefault` for unexpected errors within a step.
*   **(V2+):** Incorporate more advanced error handling patterns like retries or global error handlers when available [1].

## 8. Readability & Maintainability

*   **Comments:** Add comments (`#`) to explain workflow logic, complex mappings, or the purpose of specific steps/transitions.
*   **Formatting:** Maintain consistent YAML indentation and formatting.
*   **Workflow Size:** If a workflow becomes overly large and complex, consider opportunities to break it down into smaller, potentially reusable subworkflows (requires `subworkflow` step type support later) [1].
*   **Naming:** Use clear and consistent names for `workflowId` and `stepId`s.

## 9. Security

*   **No Sensitive Data:** **DO NOT** embed sensitive information (API keys, credentials, raw user secrets) directly within the workflow YAML definition. Use `context.configuration` variables (injected securely by the framework) or dedicated secure MCP tools.