# Sandbox API Implementation Standards (`02-sandbox-api.md`)

This document outlines standards for implementing the internal `/execute` API server within UHLP Sandbox containers (JIT Runners, LLM Orchestrator/Runners). Consistency here is vital for reliable interaction with the Core Framework.

## 1. API Specification Adherence

*   **Strict Conformance:** The implementation **MUST** strictly adhere to the **`Core Framework -> Sandbox API Specification (Version 1.0)`** [1]. This includes:
    *   Endpoint: `POST /execute`
    *   Transport: HTTP/1.1
    *   Headers: Correct usage of `Content-Type`, `Accept`, `X-Request-ID`.
    *   Request Body: Parsing and validation according to the specified JSON structure (`requestId`, `requestData`, `context`).
    *   Response Body: Formatting according to the specified JSON structure (`requestId`, `resultType`, `data`, `metrics`).
    *   HTTP Status Codes: Correct usage for transport-level vs. application-level success/failure.

## 2. HTTP Server Implementation

*   **Lightweight Framework:** Use a minimal, efficient HTTP server framework suitable for the sandbox's language (e.g., Python's `http.server`, `FastAPI` in minimal config; Node.js's built-in `http`, `Fastify`). Avoid heavyweight frameworks unless strictly necessary.
*   **Port Configuration:** The listening port should be configurable via environment variables (e.g., `UHLP_SANDBOX_PORT`, default 8080).
*   **Basic Health Check:** Implement a simple `GET /healthz` endpoint that returns HTTP 200 OK if the server is running and able to process requests. This aids the `SandboxManager` [1].
*   **Framework Endpoint:** Consider implementing a `POST /_framework/load_code` endpoint (or similar) if required for future "Server Mode" JIT execution needing hot-reloading signals (though V0.1 assumes "Interpreter Mode") [1].

## 3. Request Handling & Validation

*   **Parse Request:** Safely parse the incoming JSON request body. Handle JSON parsing errors gracefully (return HTTP 400 Bad Request).
*   **Validate Core Fields:** Validate the presence and basic types of `requestId`, `requestData`, `context`, `requestData.source`, and `context.mcp_endpoint`. Return HTTP 400 if essential fields are missing/invalid.
*   **Route by `source`:** The primary logic branching should typically be based on `requestData.source` to handle HTTP requests, internal triggers, queue messages, etc., appropriately [1].
*   **Validate `taskDetails` / `workflowInfo`:** If executing JIT code or workflows, validate the relevant details received in the context (e.g., script path exists, workflow ID is known).

## 4. Logic Execution (JIT/LLM/Workflow)

*   **JIT ("Interpreter Mode" V0.1):** [1]
    *   Identify the target `script` and `function` from `context.componentId` lookup or `taskDetails` received.
    *   Verify the script file exists on the shared volume mount based on the path provided. Handle "file not found" errors.
    *   Prepare input for the script (e.g., serialize relevant parts of `requestData` and `context` as JSON, pass via stdin or temporary file).
    *   Execute the script using the appropriate language interpreter (`python <script_path> <function_name> ...`).
    *   Capture `stdout`, `stderr`, and `exitCode`. Parse `stdout` (expected to be JSON or the defined result) to get the result data. Handle non-zero `exitCodes` or parsing failures as execution errors.
*   **LLM (Prompt Template):** [1]
    *   Identify the `promptTemplate` path from `context.componentId` lookup or `taskDetails`.
    *   Load the template file using the state access mechanism (likely `core.state.getDefinitionFileContent` via MCP) [1].
    *   Prepare the Jinja2 rendering context using `requestData` and `context` [2].
    *   Render the `template` string.
    *   Construct the parameters for the `core.llm.generate` MCP call (merging defaults from template, step overrides).
    *   Invoke `core.llm.generate` via MCP [1].
    *   Handle the MCP response. If `outputSchema` is defined in the template, validate the LLM completion against the schema [2]. Report validation failures as application errors (`resultType: 'error'`).
*   **Workflow Orchestration:** [1]
    *   Identify the `workflowId` from `context.workflowInfo`.
    *   Load the workflow YAML definition using `core.state.getDefinitionFileContent` via MCP [1].
    *   Initialize workflow execution state (current step, accumulated data).
    *   Iterate through steps based on the YAML definition (`startAt`, `transitions`):
        *   Prepare `inputMapping` for the current step.
        *   Execute the step based on its `type` (`jit`, `llm`, `mcp`, `control`), potentially making MCP calls for `llm`, `jit`, `mcp` types [1].
        *   Handle step success/failure and evaluate `transitions` to determine the next step.
        *   Manage workflow state consistently between steps (potentially using `core.state.setRuntimeValue/getRuntimeValue` via MCP for complex state).
    *   Upon reaching a terminal step (`end: true`), format the final result [1].

## 5. MCP Interaction

*   **Use Provided Endpoint:** Always use the `context.mcp_endpoint` URL provided in the `/execute` request for all MCP calls [1].
*   **Standard Calls:** Make MCP calls using simple HTTP POST requests with a JSON body like `{ "tool": "tool.name", "params": { ... } }`.
*   **Error Handling:** Handle potential errors from MCP calls (network errors, non-200 responses, errors indicated in the MCP response body). Decide whether to retry (if appropriate and configured) or fail the current execution step. Log MCP call details and errors.
*   **Pass Context:** Ensure necessary context (like `appId`, potentially `traceId`) is implicitly handled or explicitly passed if required by the MCP call structure (TBD).

## 6. Response Formatting

*   **Consistent Structure:** Always return a JSON body matching the specification, including `requestId` [1].
*   **`resultType`:** Set `resultType` accurately based on the outcome (`generic`, `httpResponse`, `error`, `workflowStep`) [1].
*   **`data`:** Structure the `data` field according to the chosen `resultType` [1]. For `httpResponse`, ensure `bodyEncoding` is set correctly if using Base64.
*   **`metrics`:** Populate the `metrics` field with relevant performance data (execution time, counts of specific operations, LLM token usage) using the OTLP-inspired format expected by the `MetricCollector` [1].

## 7. Error Reporting

*   **Internal Errors:** Unhandled exceptions or crashes within the sandbox code (e.g., Python exceptions, Node.js errors) should result in an HTTP 500 response being sent back to the framework, ideally with error details logged using the MCP logging tool.
*   **Application Errors:** Expected business logic errors (e.g., validation failed, resource not found, insufficient permissions) should be handled gracefully and reported back to the framework using `resultType: 'error'` with a structured `data` field (`code`, `message`, `details`) [1].

## 8. Logging

*   **Use MCP:** Use the `core.framework.logFrameworkMessage` MCP tool for all logging [1]. Avoid writing directly to `stdout`/`stderr` unless essential for bare-minimum crash diagnostics.
*   **Contextual Logging:** Include relevant context in log messages (e.g., `appId`, `componentId`, `requestId`, current workflow step).
*   **Log Levels:** Use appropriate log levels (`debug`, `info`, `warn`, `error`).

## 9. Security

*   **Trust Boundary:** Treat data received in the `/execute` call (especially `requestData`) as potentially untrusted, even though it comes from the Core Framework. Perform necessary validation specific to the task.
*   **MCP Tool Usage:** Use MCP tools as intended. Do not attempt to bypass MCP for direct access to resources unless explicitly permitted by the design (unlikely). Be mindful of parameters passed to tools like `core.linux.executeCommand`.
*   **Dependency Management:** Keep sandbox dependencies updated and scan for vulnerabilities if custom libraries are included in sandbox images.

## 10. Performance

*   **Efficiency:** Write reasonably efficient code, especially for JIT tasks or workflow orchestration logic. Avoid unnecessary computations or blocking operations.
*   **Resource Usage:** Be mindful of memory and CPU usage within the sandbox.