from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from enum import Enum

# Aligning with potential UHLP standard (Python 3.10+)
# from typing import TypeAlias # For Python 3.10+

# --- Helper Types ---
# RequestData: TypeAlias = Dict[str, Any] # For Python 3.10+
# Context: TypeAlias = Dict[str, Any] # For Python 3.10+

RequestData = Dict[str, Any] # Using Dict for broader compatibility
Context = Dict[str, Any] # Using Dict for broader compatibility

# --- Core Data Structures ---

@dataclass
class RouteMatcher:
    """Defines criteria for matching incoming HTTP requests to a component."""
    path_pattern: str # e.g., "/api/users/:id"
    methods: List[str] # e.g., ["GET", "POST"]

class HandlerType(Enum):
    """Specifies the execution mechanism for a component."""
    UNSPECIFIED = 0
    LLM = 1
    JIT = 2
    WORKFLOW = 3

@dataclass
class ComponentDefinition:
    """Defines a specific logical part of an application (e.g., an API endpoint handler, a workflow)."""
    component_id: str # Unique ID for this logical component/handler/workflow
    handler_type: HandlerType # LLM, JIT, WORKFLOW
    target_pool_name: str # Which sandbox pool handles this
    task_details: Dict[str, Any] = field(default_factory=dict) # Details specific to the handlerType
                                                              # e.g., { "script": "...", "function": "..." } for JIT
                                                              # e.g., { "prompt_template": "..." } for LLM
                                                              # e.g., { "workflowId": "..." } for WORKFLOW
    expected_result_format: str = "generic" # "generic" | "httpResponse" | "error"
    route_matcher: Optional[RouteMatcher] = None # Optional: If triggered by HTTP requests
    configuration_overrides: Dict[str, Any] = field(default_factory=dict) # Component-specific config

@dataclass
class ResourceLimits:
    """Resource limits for a sandbox container."""
    cpu_limit: str # e.g., "0.5"
    memory_limit: str # e.g., "512M"

@dataclass
class PoolDefinition:
    """Defines a pool of identical sandbox container instances."""
    pool_name: str # e.g., "python_runner", "llm_orchestrator"
    docker_image: str # Specific Docker image to use for this pool
    min_instances: int = 1 # Minimum desired running instances
    max_instances: int = 1 # Maximum allowed running instances (for scaling)
    resource_limits: Optional[ResourceLimits] = None # CPU/Memory limits for containers
    volume_mounts: List[str] = field(default_factory=list) # Volume mounts needed (e.g., for code, state access)
    sandbox_type: str = "docker" # e.g., "docker", "firecracker" (Future)

@dataclass
class SandboxPoolConfig:
    """Requirements for the Sandbox Manager for an application."""
    pools: List[PoolDefinition] = field(default_factory=list)

@dataclass
class ApiKeyDefinition:
    """Defines an API key for authentication and authorization."""
    key_hash: str # Hash of the key
    description: str
    permissions: List[str] = field(default_factory=list) # Permissions associated
    enabled: bool = True

@dataclass
class InterAppPermission:
    """Defines permission for one application to interact with another."""
    allowed_source_app_id: str
    allowed_events: List[str] = field(default_factory=list) # e.g., ["http:/api/trigger", "trigger:new_data"]

@dataclass
class UserRoleDefinition:
    """Defines a user role and its associated permissions within an application."""
    role_name: str
    permissions: List[str] = field(default_factory=list)

@dataclass
class SecurityConfig:
    """Security configuration for an application."""
    api_keys: List[ApiKeyDefinition] = field(default_factory=list)
    inter_app_permissions: List[InterAppPermission] = field(default_factory=list)
    user_roles: Dict[str, UserRoleDefinition] = field(default_factory=dict) # Map role name to definition

@dataclass
class MetricCondition:
    """Defines a condition based on metrics for optimization rules."""
    expression: str # e.g., "avg(latency_ms) > 1000 && count(requests) > 600"

class OptimizationAction(Enum):
    """Defines the action to take when an optimization rule is triggered."""
    UNSPECIFIED = 0
    TRIGGER_JIT = 1
    RECOMMEND_JIT = 2
    # ... other actions ...

@dataclass
class OptimizationRule:
    """Defines a rule for the OptimizationOracle."""
    description: str
    condition: MetricCondition
    action: OptimizationAction
    action_params: Dict[str, Any] = field(default_factory=dict) # Params for the action
    prefer_llm_flexibility: bool = False # Hint for the Oracle

@dataclass
class OptimizationConfig:
    """Optimization configuration for an application."""
    enabled: bool = True
    rules: List[OptimizationRule] = field(default_factory=list) # Global/App-level rules

@dataclass
class StateConfig:
    """Configuration for the application's state storage."""
    type: str # e.g., "git_yaml"
    params: Dict[str, str] = field(default_factory=dict) # e.g., {"repo_url": "...", "base_path": "state/"}

@dataclass
class AppDefinition:
    """The comprehensive definition of a UHLP application."""
    app_id: str # User-provided or framework-generated unique ID
    display_name: str
    version: str = "0.1.0"
    sandbox_pools: SandboxPoolConfig = field(default_factory=SandboxPoolConfig) # Requirements for the Sandbox Manager
    state_store_config: StateConfig = field(default_factory=StateConfig) # How state is stored
    component_registry: Dict[str, ComponentDefinition] = field(default_factory=dict) # Map of componentId to definition
    security_config: SecurityConfig = field(default_factory=SecurityConfig) # API Keys, inter-app permissions
    configuration: Dict[str, Any] = field(default_factory=dict) # Default app-level config values
    optimization_config: OptimizationConfig = field(default_factory=OptimizationConfig) # Rules for OptimizationOracle
    # ... other metadata ...

# --- Structures for Sandbox /execute API ---

@dataclass
class HttpRequestDetails:
    """Details for an HTTP source request."""
    method: str
    path: str
    route_pattern: Optional[str] = None
    path_parameters: Dict[str, str] = field(default_factory=dict)
    query_parameters: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    body_encoding: str = "utf8" # "utf8" | "base64"

@dataclass
class TriggerDetails:
    """Details for an internal trigger source."""
    source_app_id: str
    trigger_event: str
    payload: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CallbackDetails:
    """Details for a callback source."""
    callback_url: str
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    body_encoding: str = "utf8"

@dataclass
class QueueDetails:
    """Details for a queue message source."""
    queue_name: str
    message_id: str
    payload: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CronDetails:
    """Details for a cron job source."""
    job_id: str
    scheduled_time: str # ISO 8601 timestamp

@dataclass
class RequestData:
    """Details of the event triggering execution in a sandbox."""
    source: str # "http" | "trigger" | "callback" | "queue" | "cron" | "internal"
    http_details: Optional[HttpRequestDetails] = None
    trigger_details: Optional[TriggerDetails] = None
    callback_details: Optional[CallbackDetails] = None
    queue_details: Optional[QueueDetails] = None
    cron_details: Optional[CronDetails] = None
    # Add other details fields as needed for 'internal', etc.

@dataclass
class UserInfo:
    """Information about the authenticated user."""
    id: str
    roles: List[str] = field(default_factory=list)
    is_authenticated: bool = False
    claims: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowInfo:
    """Information about the workflow being executed."""
    workflow_id: str
    start_at: Optional[str] = None # Optional starting step ID

@dataclass
class Context:
    """Background information provided by the Framework to a sandbox."""
    app_id: str # Unique ID of the UHLP application
    component_id: str # ID of the component/workflow being invoked
    workflow_info: Optional[WorkflowInfo] = None # Optional: Added if handlerType is WORKFLOW
    mcp_endpoint: str # URL for the App-Specific MCP Server
    state_config: StateConfig # Info about how the sandbox should access its state
    user_info: Optional[UserInfo] = None # Optional: Present if user context is available/authenticated
    session_id: Optional[str] = None # Optional: Identifier for framework-managed session state
    configuration: Dict[str, Any] = field(default_factory=dict) # Select app-specific config values injected by Framework
    application_info: Dict[str, Any] = field(default_factory=dict) # General info about the running app (e.g., deployment_mode)

# --- Structures for Sandbox /execute API Response ---

@dataclass
class HttpResponseDetails:
    """Details for an HTTP response result type."""
    status_code: int
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    body_encoding: str = "utf8" # "utf8" | "base64"

@dataclass
class ErrorDetails:
    """Details for an application-level error result type."""
    code: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowStepResult:
    """Intermediate result from a workflow step execution."""
    workflow_id: str
    step_id: str
    status: str # "completed" | "failed"
    output: Dict[str, Any] = field(default_factory=dict) # Data produced by this step
    error: Optional[ErrorDetails] = None # Optional error details if status is failed

@dataclass
class SandboxMetrics:
    """Performance metrics from the Sandbox."""
    execution_time_ms: Optional[int] = None
    mcp_calls: List[Dict[str, Any]] = field(default_factory=list) # List of MCP call summaries
    # Other relevant sandbox-internal metrics

@dataclass
class SandboxExecuteResponse:
    """Response body from the Sandbox /execute endpoint."""
    request_id: str
    result_type: str # "generic" | "httpResponse" | "error" | "workflowStep"
    data: Dict[str, Any] = field(default_factory=dict) # Structure depends on result_type
    metrics: Optional[SandboxMetrics] = None
