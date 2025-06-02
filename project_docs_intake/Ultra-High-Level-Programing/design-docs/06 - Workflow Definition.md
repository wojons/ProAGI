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
    # Supported V1 types: jit, llm, mcp, control <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
    type: jit
    # Optional: Human-readable description of the step's purpose.
    description: Validate the incoming order payload against the required JSON schema.
    # Required (for most types): Defines the specific resource or action being invoked.
    # Structure varies based on 'type'.
    target:
      # For 'jit' type:
      language: python # Specifies the required JIT runner language/pool <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
      script: "_jit_code/validators/order_validator.py" # Path to the JIT script file <source_id data="1" title="https://docs.cline.bot/improving-your-prompting-skills/prompting" />
      function: "validate_schema" # Function within the script to execute
    # Required: Defines how to construct the input data for this step.
    # Uses the Workflow Expression Syntax (see 6.1.5) to map data from the trigger or previous steps.
    inputMapping:
      orderData: trigger.requestData.httpDetails.body # Pass the raw HTTP body
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

- **`jit`:** Executes a predefined function within a JIT code script [1].
    - `target`: Must specify `language`, `script` path, and `function` name.
    - **Execution:** The workflow orchestrator packages the inputs defined by `inputMapping` and uses an MCP call (back to the framework/`RequestRouter`) to request execution of this specific JIT function in an appropriate sandbox pool. The result is returned via the MCP response [1].
- **`llm`:** Interacts with a Large Language Model [1].
    - `target`: Must specify `promptTemplate` (path to a YAML prompt template file, see Section 8.1) or inline `prompt`. Can optionally override `model` and LLM `parameters`.
    - **Execution:** The orchestrator loads the prompt template (if specified), renders it using Jinja2 and inputs from `inputMapping`, then calls the `core.llm.generate` MCP tool [1]. The validated (against `outputSchema` if provided) LLM response becomes the step's output [1, 2].
- **`mcp`:** Directly invokes a tool available via the Model Context Protocol [1].
    - `target`: Must specify the full `tool` name (e.g., `community.database.postgres.query`, `core.linux.executeCommand`).
    - **Execution:** The orchestrator formats the parameters based on `inputMapping` and makes the specified MCP tool call via its `mcp_endpoint`. The result of the MCP call becomes the step's output [1].
- **`control`:** Performs internal workflow logic or data manipulation without external calls [1]. Requires a `subtype` for specific behavior:
    - `formatResponse`: (V1) Prepares the final data structure to be returned as the overall workflow result, defining the `resultType` and `data` for the `RequestRouter` [1]. Should have `transitions: { end: true }`.
    - **(Future/V2 Placeholders inspired by n8n [1]):**
        - `loop`: Iterates over a list provided via `inputMapping`, executing a specified sub-step (or inline definition) for each item. Needs structure for input list, item variable name, loop body step(s).
        - `branch`: Explicit multi-way conditional branching based on `condition` expressions, directing flow to different next steps.
        - `merge`: Defines how to combine data from multiple incoming branches (relevant after `branch` or `parallel`). Needs strategies (e.g., append, merge objects).
        - `split`: Distributes processing based on conditions or item types.
        - `wait`: Pauses workflow execution (e.g., for a fixed duration, until a specific time, until an external event/webhook is received via framework).
        - `subworkflow`: Calls another `workflowId` as a self-contained unit, passing inputs and receiving outputs.

#### 6.1.5. Expression Syntax (V1 - Simple JSONPath-like / Dot Notation)

A simple expression syntax is used within `inputMapping` (to define data sources) and `transitions` `condition`s (to evaluate boolean logic) [1].

- **Data Access:** Uses dot notation to access data originating from:
    - `trigger.*`: The initial event data (structure depends on `trigger.type`, mirroring `requestData`) [1].
    - `steps.<stepId>.output.*`: The entire output object of a previously executed step [1]. Can access nested properties (`steps.stepA.output.user.address.city`). Array access via index (`steps.stepB.output.results[0]`).
    - `step.output.*`: Within `transitions`, accesses the output of the _current_ step (useful for checking success/failure details or immediate output values) [1].
    - `context.*`: Data from the `context` object provided in the initial `/execute` call (`context.userInfo.id`, `context.configuration.someKey`) [1].
    - `workflow.*`: (TBD V1/V2) Workflow-level context like `workflow.id`, `workflow.startTime`, potential shared variables, `workflow.lastError`.
- **Literals:** String literals must be enclosed in single quotes (`'hello'`, `'SELECT *'`). Numbers (`123`, `0.5`) and booleans (`true`, `false`) are used directly [1].
- **Conditions (`condition` field):** Support basic comparisons (`==`, `!=`, `>`, `<`, `>=`, `<=`) and logical operators (`&&` - AND, `||` - OR, `!` - NOT). Parentheses `()` can be used for grouping. An existence check function `defined(path.to.optional.field)` might be useful [1].
- **Scope:** Expressions assume data is JSON-like. V1 focuses on basic retrieval and boolean logic. More complex transformations (string manipulation, array filtering) might require a dedicated `jit` step or richer expression functions in V2 [1].

#### 6.1.6. Transitions & Flow Control (`onSuccess`, `onFailure`, `condition`, `end`)

The `transitions` block within a step definition dictates the workflow's execution path after the step completes [1].

- **Evaluation Order:** If multiple conditional transitions are defined (e.g., within `onFailure` or as a list under `transitions`), they are evaluated sequentially. The first condition that evaluates to `true` determines the `nextStep`.
- **Success Path (`onSuccess`):** A shorthand specifying the `stepId` to transition to if the current step completes successfully (e.g., JIT function returns non-error, MCP call succeeds, LLM call returns valid output).
- **Failure Handling (`onFailure`, `onFailureDefault`):**
    - `onFailure`: An optional list of conditional transitions specifically for handling _internal failures_ within the step execution (e.g., JIT code throws exception, MCP tool returns error, LLM validation fails). Each entry requires a `condition` (often referencing `step.output.error.*`) and a `nextStep`.
    - `onFailureDefault`: Specifies the `stepId` to transition to if the step fails internally _and_ no `onFailure` condition matched. If omitted and failure occurs, workflow execution may halt with an error.
- **Unified `transitions` Array (Alternative/Preferred Structure):**
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
- This array structure provides more flexibility than separate `onSuccess`/`onFailure` blocks.
- **Ending the Workflow (`end: true`):** A transition target of `end: true` signifies that the workflow execution should terminate after this step. Terminal steps (both success and error handling paths) must include this in their transitions [1]. The output of the final step before `end: true` typically becomes the overall result provided back to the `RequestRouter` (especially if formatted by a `control.formatResponse` step).

### 6.2. Execution Model

1. The `RequestRouter` identifies that a trigger matches a `WORKFLOW` handler type [1].
2. It allocates an appropriate orchestrator sandbox (JIT Runner or LLM) and sends the `/execute` call, including `context.workflowInfo { workflowId }` [1].
3. The orchestrator sandbox receives the call, extracts the `workflowId`, and loads the corresponding Workflow YAML file using `core.state.getDefinitionFileContent` [1].
4. It starts execution at the step defined by `startAt` [1].
5. For each step:
    - It resolves inputs using `inputMapping` and the current data context (trigger + previous step outputs).
    - It executes the step based on its `type` (invoking JIT via MCP, calling LLM via MCP, calling MCP directly, or processing control logic) [1].
    - It stores the step's output.
    - It evaluates the `transitions` block to determine the `nextStep` ID [1].
6. Execution continues until a step transitions to `end: true` [1].
7. The output of the final step is formatted and returned as the result of the initial `/execute` call [1].

### 6.3. Enhancements Inspired by n8n (V2+ Considerations)

While V1 focuses on the core structure, future versions should incorporate more advanced flow control and data handling concepts inspired by mature tools like n8n [1]:

- **Robust Looping:** Implementing dedicated `loop` constructs [1].
- **Parallel Execution:** Adding a `parallel` step/block to run multiple branches concurrently.
- **Advanced Merging/Splitting:** Defining explicit strategies for handling data across branches [1].
- **Subworkflows:** Allowing workflows to call other workflows modularly [1].
- **Sophisticated Error Handling:** Implementing configurable retries, dead-letter queues, `try/catch`-like blocks within the YAML [1].
- **Wait States:** Adding explicit `wait` steps for timed delays or external event triggers [1].
- **Richer Expression Language:** Enhancing the expression syntax with more built-in functions for data transformation [1].
- **Item Linking / Context:** More explicit ways to manage data context across iterations or branches [1].
