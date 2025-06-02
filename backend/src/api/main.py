from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles # Import StaticFiles
from fastapi.responses import HTMLResponse # Import HTMLResponse
from typing import Optional, Dict, Any, List
import uuid # For generating request IDs if not provided
import time # For timestamps

# Import necessary data models from core.shared.data_models
from core.shared.data_models.data_models import (
    RequestPayload,
    ResponsePayload,
    AppDefinition,
    ToolDefinition,
    ServerStatus,
    SandboxStatus,
    LogMessage,
    Metric,
    User, # Import User data model
    # Import other relevant data models as needed for API endpoints
)

# Import database dependency
from backend.src.db.database import get_session # Import get_session dependency
from backend.src.db.models import User as DBUser # Import DB User model to avoid naming conflict
from sqlmodel import Session, select # Import Session and select for database operations
import bcrypt # Import bcrypt for password hashing

# Import interfaces for core services
from core.interfaces.application_registry_interface import ApplicationRegistryInterface
from core.interfaces.request_router_interface import RequestRouterInterface
from core.interfaces.tool_manager_interface import ToolManagerInterface
from core.interfaces.logging_service_interface import LoggingServiceInterface
from core.interfaces.metric_collector_interface import MetricCollectorInterface
from core.interfaces.mcp_hub_interface import McpHubInterface
from core.interfaces.state_manager_interface import StateManagerInterface
from core.interfaces.sandbox_manager_interface import SandboxManagerInterface
from core.interfaces.sandbox_api_interface import SandboxAPIInterface
from core.interfaces.optimization_oracle_interface import OptimizationOracleInterface
from core.interfaces.event_bus_interface import EventBusInterface # Import EventBusInterface

# Import the instantiated core service instances from the main entry point
# These instances are created and wired together in backend.src.main
from backend.src.main import (
    state_manager_instance,
    logging_service_instance,
    metric_collector_instance,
    mcp_hub_instance,
    app_registry_instance,
    tool_manager_instance,
    sandbox_manager_instance,
    sandbox_api_instance,
    request_router_instance, # Import the RequestRouter instance
    optimization_oracle_instance,
    event_bus_instance, # Import the EventBus instance
)


# --- Dependency Injection Setup ---
# Use FastAPI's built-in Depends with provider functions that return the
# globally instantiated core service instances from backend.src.main.

# Dependency provider functions
def get_state_manager() -> StateManagerInterface:
    """Provides the StateManager instance."""
    return state_manager_instance

def get_logging_service() -> LoggingServiceInterface:
    """Provides the LoggingService instance."""
    return logging_service_instance

def get_metric_collector() -> MetricCollectorInterface:
    """Provides the MetricCollector instance."""
    return metric_collector_instance

def get_mcp_hub() -> McpHubInterface:
    """Provides the McpHub instance."""
    return mcp_hub_instance

def get_app_registry() -> ApplicationRegistryInterface:
    """Provides the ApplicationRegistry instance."""
    return app_registry_instance

def get_tool_manager() -> ToolManagerInterface:
    """Provides the ToolManager instance."""
    return tool_manager_instance

def get_sandbox_manager() -> SandboxManagerInterface:
    """Provides the SandboxManager instance."""
    return sandbox_manager_instance

def get_sandbox_api() -> SandboxAPIInterface:
    """Provides the SandboxAPI client instance."""
    return sandbox_api_instance

def get_request_router() -> RequestRouterInterface:
    """Provides the RequestRouter instance."""
    return request_router_instance

def get_optimization_oracle() -> OptimizationOracleInterface:
    """Provides the OptimizationOracle instance."""
    return optimization_oracle_instance

def get_event_bus() -> EventBusInterface:
    """Provides the EventBus instance."""
    return event_bus_instance


# --- FastAPI App Instance ---
app = FastAPI(
    title="Nexus CoCreate AI API",
    description="API for the Nexus CoCreate AI Web-Based AI Coding Environment.",
    version="0.1.0", # Initial version for POC
)

# --- Serve Static Files and Frontend HTML ---
# Mount the static directory to serve CSS, JS, etc.
app.mount("/static", StaticFiles(directory="backend/src/frontend/static"), name="static")

# Serve the index.html file at the root
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("backend/src/frontend/index.html") as f:
        return HTMLResponse(content=f.read())


# --- API Routers ---

# Applications Router
applications_router = APIRouter(prefix="/applications", tags=["applications"])

@applications_router.post("/register")
async def register_application(
    definition: AppDefinition,
    app_registry: ApplicationRegistryInterface = Depends(get_app_registry)
):
    """Registers a new application."""
    print(f"Received request to register application: {definition.appId}") # Basic logging
    # TODO: Add input validation (Issue #XX)
    # TODO: Add authentication and authorization (Issue #XX)

    response = await app_registry.register_application(definition)
    if response.get("success"):
        return response
    # TODO: Handle specific error cases (e.g., conflict) and return appropriate HTTP status codes
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.get("message", "Failed to register application"))

@applications_router.put("/{appId}")
async def update_application(
    appId: str,
    updated_fields: Dict[str, Any], # TODO: Use a specific update model instead of Dict[str, Any]
    app_registry: ApplicationRegistryInterface = Depends(get_app_registry)
):
    """Updates an existing application's definition."""
    print(f"Received request to update application: {appId}") # Basic logging
    # TODO: Add input validation (Issue #XX)
    # TODO: Add authentication and authorization (Issue #XX)

    # TODO: Implement update_mask logic if needed
    response = await app_registry.update_application(appId, None, updated_fields)
    if response.get("success"):
        return response
    # TODO: Handle specific error cases (e.g., not found)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.get("message", "Failed to update application"))

@applications_router.delete("/{appId}")
async def deregister_application(
    appId: str,
    delete_state: bool = False,
    app_registry: ApplicationRegistryInterface = Depends(get_app_registry)
):
    """Deregisters an application."""
    response = await app_registry.deregister_application(appId, delete_state)
    if response.get("success"):
        return response
    # TODO: Handle specific error cases (e.g., not found)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.get("message", "Failed to deregister application"))

@applications_router.get("/{appId}/status")
async def get_application_status(
    appId: str,
    app_registry: ApplicationRegistryInterface = Depends(get_app_registry)
):
    """Gets the status of a specific application."""
    response = await app_registry.get_application_status(appId)
    # Assuming get_application_status always returns a status dict even if app not found,
    # but status field indicates state (e.g., "unspecified" or "not_found")
    if response: # Check if response is not None/empty
         # TODO: Check response structure and status field to determine if app was found
         # For now, just return the response
         return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Application '{appId}' not found")


@applications_router.get("/")
async def list_applications(
    app_registry: ApplicationRegistryInterface = Depends(get_app_registry)
):
    """Lists all active applications."""
    # TODO: ApplicationRegistry.list_active_applications returns Dict[str, Any] for POC, should return List[AppStatus] or similar
    response = await app_registry.list_active_applications()
    # Assuming the response contains a list of applications under a "applications" key
    return response.get("applications", []) # Return the list of applications


# Requests Router
requests_router = APIRouter(prefix="/requests", tags=["requests"])

@requests_router.post("/route")
async def route_request(
    request_payload: RequestPayload,
    request_router: RequestRouterInterface = Depends(get_request_router)
):
    """Routes an incoming request to the appropriate application component."""
    # Ensure request_id is present, generate if not
    if not request_payload.requestId:
        request_payload.requestId = str(uuid.uuid4())

    response = await request_router.route_request(request_payload)
    if response.success:
        return response
    # TODO: Handle specific error cases from RequestRouter (Issue #XX)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response.message) # Assuming message contains error details


# Tools Router
tools_router = APIRouter(prefix="/tools", tags=["tools"])

@tools_router.get("/")
async def list_tools(
    tool_manager: ToolManagerInterface = Depends(get_tool_manager)
):
    """Lists all available tools."""
    tools_list = await tool_manager.list_tools()
    return tools_list # Assuming list_tools returns List[ToolDefinition]


@tools_router.get("/{tool_name}")
async def get_tool_definition(
    tool_name: str,
    tool_manager: ToolManagerInterface = Depends(get_tool_manager)
):
    """Gets the definition of a specific tool."""
    tool_def = await tool_manager.get_tool_definition(tool_name)
    if tool_def:
        return tool_def # Assuming get_tool_definition returns Optional[ToolDefinition]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tool '{tool_name}' not found")


# Status Router
status_router = APIRouter(prefix="/status", tags=["status"])

@status_router.get("/")
async def get_system_status(
    app_registry: ApplicationRegistryInterface = Depends(get_app_registry),
    mcp_hub: McpHubInterface = Depends(get_mcp_hub),
    sandbox_manager: SandboxManagerInterface = Depends(get_sandbox_manager),
    state_manager: StateManagerInterface = Depends(get_state_manager), # Add StateManager dependency
    logging_service: LoggingServiceInterface = Depends(get_logging_service), # Add LoggingService dependency
    metric_collector: MetricCollectorInterface = Depends(get_metric_collector), # Add MetricCollector dependency
    event_bus: EventBusInterface = Depends(get_event_bus), # Add EventBus dependency
    optimization_oracle: OptimizationOracleInterface = Depends(get_optimization_oracle), # Add OptimizationOracle dependency
):
    """Gets the overall system status."""
    # For POC, aggregate status from key components
    app_statuses = await app_registry.list_active_applications() # Assuming this returns a list of statuses
    server_statuses = await mcp_hub.list_servers() # Assuming this returns List[ServerStatus]
    # TODO: Get sandbox statuses from SandboxManager (maybe a list_all_sandboxes method needed) (Issue #XX)
    # sandbox_statuses = await sandbox_manager.list_all_sandboxes() # Assuming such a method exists

    # TODO: Get status from other services (StateManager, EventBus, LoggingService, OptimizationOracle)
    # This might require adding status methods to their interfaces/implementations. (Issue #XX)
    state_manager_status = {"status": "unknown"} # Placeholder
    logging_service_status = {"status": "unknown"} # Placeholder
    metric_collector_status = {"status": "unknown"} # Placeholder
    event_bus_status = {"status": "unknown"} # Placeholder
    optimization_oracle_status = {"status": "unknown"} # Placeholder


    return {
        "status": "ok", # TODO: Determine overall status based on component statuses (Issue #XX)
        "applications": app_statuses,
        "mcp_servers": server_statuses,
        # "sandboxes": sandbox_statuses,
        "state_manager": state_manager_status,
        "logging_service": logging_service_status,
        "metric_collector": metric_collector_status,
        "event_bus": event_bus_status,
        "optimization_oracle": optimization_oracle_status,
    }


# Users Router
users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.post("/register")
async def register_user(
    user: User, # Use the User data model for request body
    db_session: Session = Depends(get_session) # Inject database session
):
    """Registers a new user."""
    print(f"Received request to register user: {user.username}") # Basic logging
    # TODO: Add input validation (Issue #XX)

    # Check if username or email already exists
    existing_user = db_session.exec(select(DBUser).where(DBUser.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    # TODO: Check for existing email if email is required to be unique (Issue #XX)

    # Hash the password
    hashed_password = bcrypt.hashpw(user.hashed_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create new DBUser instance
    db_user = DBUser(
        user_id=str(uuid.uuid4()), # Generate a unique user ID
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        is_active=True, # New users are active by default
        roles=",".join(user.roles) if user.roles else "", # Store roles as comma-separated string
        created_at=str(time.time()), # Use timestamp for creation time
        updated_at=str(time.time()) # Use timestamp for update time
    )

    try:
        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)
        print(f"User '{user.username}' registered successfully with ID: {db_user.user_id}") # Basic logging
        return {"success": True, "user_id": db_user.user_id}
    except Exception as e:
        db_session.rollback()
        print(f"Error during user registration for {user.username}: {e}") # Basic error logging
        # TODO: Log this error properly (Issue #XX)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to register user: {e}")


@users_router.post("/login")
async def login_user(
    user: User, # Use User model for login credentials (only username/password needed)
    db_session: Session = Depends(get_session) # Inject database session
):
    """Logs in a user and returns an authentication token."""
    print(f"Received request to login user: {user.username}") # Basic logging
    # TODO: Add input validation (Issue #XX)

    # Retrieve user from database by username
    db_user = db_session.exec(select(DBUser).where(DBUser.username == user.username)).first()

    if not db_user or not bcrypt.checkpw(user.hashed_password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # TODO: Generate and return an authentication token (e.g., JWT) (Issue #XX)
    # For POC, just return a success message and user ID
    print(f"User '{user.username}' logged in successfully.") # Basic logging
    return {"success": True, "message": "Login successful", "user_id": db_user.user_id}


# Include routers in the main app
app.include_router(applications_router)
app.include_router(requests_router)
app.include_router(tools_router)
app.include_router(status_router)
app.include_router(users_router) # Include the new users router

# TODO: Add event handlers for startup and shutdown (e.g., connecting to core services) (Issue #XX)
# @app.on_event("startup")
# async def startup_event():
#     # TODO: Initialize core framework components and connect to dependencies (Issue #XX)
#     # The global instances are created on import in main.py, but connections (like Redis, Docker, MCP)
#     # might need explicit async initialization here.
#     # Example: await state_manager_instance.connect_redis() # If connect method exists
#     # Example: await mcp_hub_instance.connect_initial_servers() # If connect method exists
#     pass

# @app.on_event("shutdown")
# async def shutdown_event():
#     # TODO: Clean up resources (e.g., close database connections, stop background tasks) (Issue #XX)
#     # Example: await state_manager_instance.disconnect_redis() # If disconnect method exists
#     # Example: await mcp_hub_instance.disconnect_all_servers() # If disconnect method exists
#     pass
