from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

# 4.1 Request Payload
@dataclass
class RequestPayload:
    """General structure for requests to the system."""
    method: str # e.g., "GET", "POST", "EXECUTE", "CHAT"
    path: str # e.g., "/users/123", "/execute/my-script", "/chat"
    headers: Dict[str, str] = field(default_factory=dict)
    query_params: Dict[str, str] = field(default_factory=dict)
    body: Optional[Any] = None # Request body, can be JSON, bytes, etc.
    appId: Optional[str] = None # The application ID the request is for
    taskId: Optional[str] = None # The task ID the request is related to
    requestId: Optional[str] = None # Unique ID for this request instance
    traceId: Optional[str] = None # Trace ID for the overall operation
    context: Dict[str, Any] = field(default_factory=dict) # Additional context (e.g., user info, session data)

# 4.2 Response Payload
@dataclass
class ResponsePayload:
    """General structure for responses from the system."""
    status_code: int # HTTP-like status code (e.g., 200, 201, 400, 404, 500)
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[Any] = None # Response body, can be JSON, bytes, etc.
    # TODO: Add fields for streaming responses if needed

# 4.3 ToolCall
@dataclass
class ToolCall:
    """Structure for invoking tools via MCP."""
    tool_use_id: str # Unique ID for this tool call instance
    tool_name: str # The name of the tool to execute
    arguments: Dict[str, Any] # Arguments for the tool, matching its input schema

# 4.4 ToolResult
@dataclass
class ToolResult:
    """Structure for results from tool invocations."""
    tool_use_id: str # The ID of the tool call this result corresponds to
    content: Any # The result content from the tool execution
    is_error: bool = False # True if the result indicates an error

# 4.5 Event
@dataclass
class Event:
    """Structure for events published to the EventBus."""
    event_type: str # Type of event (e.g., "log", "metric", "sandbox_status_change")
    timestamp: str # ISO 8601 timestamp
    payload: Any # Event-specific data

# 4.6 LogMessage
@dataclass
class LogMessage:
    """Standardized structure for structured log messages."""
    level: str # "debug", "info", "warn", "error", "critical"
    message: str
    appId: str
    taskId: Optional[str] = None
    requestId: Optional[str] = None
    traceId: Optional[str] = None
    timestamp: str # ISO 8601 timestamp
    context: Dict[str, Any] = field(default_factory=dict) # Additional structured context

# 4.7 AppDefinition
@dataclass
class AppDefinition:
    """Comprehensive definition of an application."""
    appId: str # Unique identifier
    name: str
    description: str
    version: str
    entryPoint: str # e.g., "sandbox://docker/imageName", "sandbox://process/command"
    roles: List[str] = field(default_factory=list)
    exposedTools: List[Dict[str, Any]] = field(default_factory=list) # TODO: Define ToolDefinition structure
    exposedResources: List[Dict[str, Any]] = field(default_factory=list) # TODO: Define ResourceDefinition structure
    dependencies: List[Dict[str, Any]] = field(default_factory=list) # TODO: Define Dependency structure
    configSchemaJson: Optional[str] = None # JSON schema string
    permissionsJson: Optional[str] = None # JSON string
    author: Optional[str] = None
    license: Optional[str] = None
    createdAt: Optional[str] = None # ISO 8601 timestamp
    updatedAt: Optional[str] = Field(default=None) # ISO 8601 timestamp
    sandboxPools: List["SandboxPoolConfig"] = field(default_factory=list) # List of sandbox pool configurations
    components: Dict[str, "ComponentDefinition"] = field(default_factory=dict) # Dictionary of component definitions
    config: Dict[str, Any] = field(default_factory=dict) # Application-specific configuration
    permissions: List["InterAppPermission"] = field(default_factory=list) # List of inter-application permissions

# 4.8 Dependency
@dataclass
class Dependency:
    """Representation of inter-component or external dependencies."""
    targetId: str # appId or MCP server ID
    type: str # "app" or "mcp_server"
    requiredVersion: Optional[str] = None # Version constraint

# 4.9 FileInfo
@dataclass
class FileInfo:
    """Metadata about a file in the state."""
    path: str
    name: str
    type: str # "file" or "directory"
    size: Optional[int] = None # Size in bytes (for files)
    createdAt: Optional[str] = None # ISO 8601 timestamp
    updatedAt: Optional[str] = None # ISO 8601 timestamp
    # TODO: Add other relevant file metadata

# 4.10 CommitInfo
@dataclass
class CommitInfo:
    """Metadata about a Git commit."""
    hash: str
    author: str
    message: str
    timestamp: str # ISO 8601 timestamp
    # TODO: Add parent hashes, etc.

# 4.11 SandboxStatus
@dataclass
class SandboxStatus:
    """Status information for a Sandbox instance."""
    sandbox_id: str # Unique ID for the sandbox instance
    appId: str # The application ID this sandbox belongs to
    status: str # e.g., "running", "stopped", "error", "initializing"
    details: Optional[str] = None # Additional status details (e.g., error message)
    createdAt: Optional[str] = None # ISO 8601 timestamp
    # TODO: Add resource usage metrics, network info, etc.

# 4.12 ToolDefinition
@dataclass
class ToolDefinition:
    """Schema for defining an MCP tool."""
    name: str
    description: str
    inputSchemaJson: str # JSON schema string
    outputSchemaJson: str # JSON schema string
    # TODO: Add other tool metadata (e.g., server_name, version)

# 4.13 ResourceDefinition
@dataclass
class ResourceDefinition:
    """Schema for defining an MCP resource."""
    uri: str # Resource URI (e.g., "state://appId/path/to/resource")
    description: str
    # TODO: Add other resource metadata (e.g., server_name, type, schema)

# 4.14 ServerStatus
@dataclass
class ServerStatus:
    """Status information for an MCP server."""
    name: str # Server name
    status: str # e.g., "connected", "disconnected", "error", "connecting"
    details: Optional[str] = None # Additional status details
    tools: List[ToolDefinition] = field(default_factory=list) # List of tools provided by this server
    resources: List[ResourceDefinition] = field(default_factory=list) # List of resources provided by this server
    # TODO: Add other server metadata (e.g., type, address)

# Metric data model (needed for MetricCollector and OptimizationOracle)
@dataclass
class Metric:
    """Structure for operational metrics."""
    name: str # Metric name (e.g., "request_duration_seconds")
    type: str # "counter", "gauge", "histogram"
    value: Optional[float] = None # Value for Gauge or Histogram, None for Counter increment
    labels: Dict[str, str] = field(default_factory=dict) # Labels for the metric

# 4.15 SandboxExecuteRequest (Proposed)
@dataclass
class SandboxExecuteRequest:
    """Request payload for executing a component within a sandbox."""
    app_id: str # The ID of the application the component belongs to
    component_id: str # The ID of the component to execute
    component_type: str # The type of component (e.g., "workflow", "prompt", "jit")
    component_definition: Any # The actual definition or code of the component (or a reference)
    input_data: Dict[str, Any] = field(default_factory=dict) # Input data for the component
    tool_access_config: Dict[str, Any] = field(default_factory=dict) # Configuration for accessing tools
    state_access_config: Dict[str, Any] = field(default_factory=dict) # Configuration for accessing state
    request_id: Optional[str] = None # Request ID for tracing
    task_id: Optional[str] = None # Task ID for tracing
    trace_id: Optional[str] = None # Trace ID for tracing
    # TODO: Add security context, user info, etc. (Issue #XX)

# 4.16 SandboxExecuteResponse (Proposed)
@dataclass
class SandboxExecuteResponse:
    """Response payload from sandbox component execution."""
    status: str # Execution status (e.g., "success", "failure", "error")
    output: Optional[Any] = None # The output of the component execution
    logs: List[str] = field(default_factory=list) # Log messages generated during execution
    metrics: Dict[str, Any] = field(default_factory=dict) # Metrics collected during execution
    tool_calls: List[ToolCall] = field(default_factory=list) # List of tool calls made by the component
    state_changes: Dict[str, Any] = field(default_factory=dict) # State changes made by the component
    error: Optional[str] = None # Error details if status is "error"

# 4.17 User (Proposed)
@dataclass
class User:
    """Represents a user of the Nexus CoCreate AI platform."""
    user_id: str # Unique identifier for the user
    username: str
    hashed_password: str
    email: Optional[str] = None
    is_active: bool = True
    roles: List[str] = field(default_factory=list) # User roles/permissions
    created_at: Optional[str] = None # ISO 8601 timestamp
    updated_at: Optional[str] = None # ISO 8601 timestamp
    # TODO: Add other user profile information (Issue #XX)

# 4.18 SandboxPoolConfig (Proposed Placeholder)
@dataclass
class SandboxPoolConfig:
    """Configuration for a pool of sandbox instances."""
    pool_id: str # Unique ID for the pool
    sandbox_type: str # e.g., "docker", "process"
    image_name: Optional[str] = None # Docker image name
    command: Optional[List[str]] = None # Command to run for process type
    min_instances: int = 0
    max_instances: int = 1
    # TODO: Add resource limits, environment variables, etc. (Issue #XX)

# 4.19 ComponentDefinition (Proposed Placeholder)
@dataclass
class ComponentDefinition:
    """Definition of an application component (workflow, prompt, JIT)."""
    component_id: str # Unique ID within the application
    type: str # "workflow", "prompt", "jit"
    definition: Any # The actual definition (e.g., YAML for workflow, string for prompt, code for JIT)
    # TODO: Add input/output schema, dependencies, configuration, etc. (Issue #XX)

# 4.20 InterAppPermission (Proposed Placeholder)
@dataclass
class InterAppPermission:
    """Defines permissions for interaction between applications."""
    target_app_id: str # The app being granted permission
    allowed_actions: List[str] = field(default_factory=list) # List of allowed actions (e.g., "execute_component", "access_state")
    # TODO: Add specific component/state path restrictions (Issue #XX)

# TODO: Define other data models as needed based on the specification (e.g., SecurityConfig, UserPermissionsForApp)
# Note: Some models might be defined as Protocol Buffer messages if used in gRPC interfaces,
# but Python dataclasses provide a good starting point for internal representation.
