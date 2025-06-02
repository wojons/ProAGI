# JIT Optimization Rules (`07-jit-optimization.md`)

This document defines the process, rules, and standards related to the Just-In-Time (JIT) optimization feature in UHLP, where LLM-based logic is dynamically replaced with more efficient JIT code (e.g., Python) [1].

## 1. Optimization Philosophy & Goals

*   **Purpose:** To improve performance (reduce latency), reduce operational cost (LLM tokens), and increase throughput for frequently used or expensive application components currently handled by LLMs [1].
*   **Trade-offs:** Recognize that JIT code is typically less flexible and harder to modify "on the fly" than LLM prompts. Optimization decisions **MUST** balance performance gains against potential loss of adaptability [1]. User experience and maintainability are key factors.
*   **Not Mandatory:** Optimization is not required for all components. Simple or infrequently used components may remain LLM-based indefinitely.

## 2. Triggering Optimization

*   **`OptimizationOracle` Role:** The `OptimizationOracle` component is responsible for analyzing metrics and applying rules to identify optimization candidates and initiate the JIT generation process [1].
*   **Metrics Source:** The Oracle primarily uses data from the `MetricCollector`, focusing on latency, LLM token usage/cost, error rates, and call frequency, grouped by `appId` and `componentId` [1].
*   **Configurable Rules (Admin Panel):** [1]
    *   Optimization rules (thresholds for metrics) **MUST** be configurable via the application's state (managed via `ApplicationRegistry` and accessible through an Admin Panel).
    *   Rules can be defined at **Global**, **Per-Application**, and **Per-Component** levels, with component-level rules overriding app-level, and app-level overriding global.
    *   Rules should include parameters like `min_latency_ms`, `min_cost_per_call`, `min_calls_per_minute`.
    *   Rules **MUST** support a flag like `prefer_llm_for_flexibility: true|false` to influence the Oracle's decision-making [1]. If `true`, the Oracle might only generate a recommendation instead of automatically triggering JIT unless thresholds are severely exceeded or triggered manually.
*   **Manual Trigger:** An explicit mechanism (via Admin Panel / `ApplicationRegistry` API) **MUST** exist to manually trigger the JIT optimization process for a specific component, bypassing automatic rule evaluation [1].

## 3. JIT Code Generation Process

*   **Initiation:** Triggered automatically by the `OptimizationOracle` based on rules, or manually via the Admin Panel [1].
*   **Specification Formulation:** The initiating process **MUST** create a detailed specification for the required JIT code. This includes:
    *   Retrieving the current LLM prompt/logic for the target `componentId`.
    *   Defining the exact input structure (based on expected `requestData`/`context`).
    *   Defining the exact output structure (based on `expectedResultFormat` / `outputSchema`).
    *   Specifying the target language (e.g., Python, configured per-app).
    *   Including relevant context or business logic derived from the prompt/existing behavior.
*   **Invoke Coder LLM:** [1]
    *   Use the `core.llm.generate` MCP tool, targeting a designated "Coder LLM" capable of high-quality code generation.
    *   Provide the detailed specification as the prompt.
    *   The prompt **MUST explicitly instruct the Coder LLM to generate BOTH the functional code AND comprehensive unit tests** (e.g., using `pytest`) with relevant test cases and mock data [1].
*   **Code Review (Recommended):** While aiming for automation, establish a process for optional human review of critical or complex generated JIT code and tests before activating it in production environments.

## 4. Artifact Management

*   **Storage:** Generated JIT code and corresponding test files **MUST** be stored within the application's versioned state directory (managed by `StateManagerInterface`) [1].
*   **Location Convention:** Use a designated subdirectory, potentially versioned (e.g., `_jit_code/<componentId>/<version>/handler.py`, `_jit_code/<componentId>/<version>/test_handler.py`). The `version` should be unique for each generation attempt.
*   **Persistence:** Use `StateManagerInterface.SetDefinitionFileContent` (or `ApplyDefinitionDiff` if managing changes) to commit these artifacts, ensuring they become part of the application's tracked state [1].

## 5. Activation & Deployment (V0.1 - Interpreter Mode)

*   **State Update:** After successfully storing the JIT artifacts, the optimization process **MUST** update the `ComponentRegistry` state for the specific `appId` and `componentId` via `StateManagerInterface.ApplyDefinitionDiff` [1].
*   **Registry Changes:** The update **MUST** change the component's `handlerType` to `jit` and update the `taskDetails` to point to the newly generated script and relevant function (e.g., `script: "_jit_code/<componentId>/<version>/handler.py", function: "handle_request"`) [1].
*   **Activation:** Subsequent requests routed by the `RequestRouter` for this component will now be directed to a JIT sandbox pool. The sandbox runner will use the updated `taskDetails` to locate and execute the new script from the shared volume (Interpreter Mode) [1].
*   **No Hot Reload Signal (V0.1):** In the V0.1 "Interpreter Mode" model, no explicit signal to running sandboxes is needed; they pick up the new script path on the next execution directed to them [1].

## 6. Generated JIT Code Standards

*   **Match Specification:** Generated code **MUST** implement the logic defined in the generation specification, correctly handling specified inputs and producing outputs matching the defined schema/format.
*   **Language Standards:** Code must adhere to the standards defined for the target language (e.g., follow `01-core-framework.md` rules if Python is the target, including formatting, linting, typing).
*   **Error Handling:** Generated code must include reasonable error handling (e.g., for invalid inputs, potential runtime issues) and return errors in the standard application error format (`resultType: 'error'`).
*   **Dependencies:** Generated code should rely only on dependencies available within the corresponding JIT sandbox environment. Avoid introducing new, unmanaged dependencies.
*   **Performance:** Generated code should be reasonably efficient for the task. Avoid obvious performance anti-patterns.
*   **Logging:** Integrate with the framework's logging via the `core.framework.logFrameworkMessage` MCP tool.

## 7. Testing Requirements

*   **Mandatory Generation:** The Coder LLM **MUST** generate unit tests alongside the functional JIT code [1].
*   **Test Coverage:** Generated tests should aim for good coverage of the generated code's logic, including edge cases and error conditions.
*   **Execution (V0.1+):** Establish a process (initially potentially manual, later automated within CI/CD or pre-deployment checks) to **execute these generated tests** against the generated code within an environment mimicking the JIT sandbox. Activation of JIT code (Step 5) should ideally be contingent on tests passing.
