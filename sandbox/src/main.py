from fastapi import FastAPI, HTTPException, status
from typing import Any, Dict, List

# Assuming data models are accessible, adjust path if they are in a shared library
# For POC, we might copy or symlink them, or install a shared core library
# For now, let's assume they are available via a relative path or installed package
# This will likely need adjustment based on the final project structure.
# from core.shared.data_models.data_models import SandboxExecuteRequest, SandboxExecuteResponse, ToolCall

# Placeholder data models if not accessible directly (remove if shared library is used)
from dataclasses import dataclass, field

@dataclass
class ToolCall:
    tool_use_id: str
    tool_name: str
    arguments: Dict[str, Any]

@dataclass
class SandboxExecuteRequest:
    app_id: str
    component_id: str
    component_type: str
    component_definition: Any
    input_data: Dict[str, Any] = field(default_factory=dict)
    tool_access_config: Dict[str, Any] = field(default_factory=dict)
    state_access_config: Dict[str, Any] = field(default_factory=dict)
    request_id: str = None
    task_id: str = None
    trace_id: str = None

@dataclass
class SandboxExecuteResponse:
    status: str
    output: Any = None
    logs: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    tool_calls: List[ToolCall] = field(default_factory=list)
    state_changes: Dict[str, Any] = field(default_factory=dict)
    error: str = None

app = FastAPI(
    title="Nexus Sandbox API",
    description="Internal API for executing application components within a sandboxed environment.",
    version="0.1.0",
)

@app.post("/execute", response_model=SandboxExecuteResponse)
async def execute_component(request: SandboxExecuteRequest):
    """
    Executes an application component within the sandbox.
    This is a placeholder implementation for the POC.
    """
    print(f"Sandbox received request to execute component: {request.component_id} for app: {request.app_id}")
    print(f"Component Type: {request.component_type}")
    print(f"Input Data: {request.input_data}")

    # TODO: Implement actual component execution logic based on component_type and component_definition (Issue #XX)
    # This would involve:
    # 1. Setting up the execution environment (e.g., loading code, initializing state).
    # 2. Running the component (e.g., Python script, workflow engine, prompt execution).
    # 3. Interacting with Core Framework API for tools, state, logging, metrics (via HTTP calls or gRPC if available).
    # 4. Collecting output, logs, metrics, tool calls, and state changes.

    # Placeholder response for POC
    if request.component_id == "error_test":
        print("Simulating an error during component execution.")
        return SandboxExecuteResponse(
            status="error",
            error="Simulated component execution error.",
            logs=["Component execution started.", "Error occurred."],
        )

    if request.component_id == "tool_call_test":
        print("Simulating a component that makes a tool call.")
        return SandboxExecuteResponse(
            status="success",
            output={"message": "Component executed, made a tool call."},
            logs=["Component execution started.", "Making tool call..."],
            tool_calls=[
                ToolCall(tool_use_id="tool_123", tool_name="example_tool", arguments={"param1": "value1"})
            ]
        )

    # Default success response
    return SandboxExecuteResponse(
        status="success",
        output={"message": f"Component '{request.component_id}' executed successfully (placeholder)."},
        logs=["Component execution started.", "Processing input...", "Component finished."],
        metrics={"execution_time_ms": 120} # Example metric
    )

if __name__ == "__main__":
    import uvicorn
    # TODO: Make host and port configurable (Issue #XX)
    uvicorn.run(app, host="0.0.0.0", port=8080) # Sandboxes often run on a different port than the main backend
