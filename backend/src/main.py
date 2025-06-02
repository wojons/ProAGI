import uvicorn # Import uvicorn to run the FastAPI app
import os # Needed for path manipulation

# Import the FastAPI app instance from the api module
from backend.src.api.main import app

# Import core component implementations
from backend.src.core.application_registry.application_registry import ApplicationRegistry
from backend.src.core.request_router.request_router import RequestRouter
from backend.src.core.sandbox_manager.sandbox_manager import SandboxManager
from backend.src.core.state_manager.state_manager import StateManager
from backend.src.core.tool_manager.tool_manager import ToolManager
from backend.src.core.mcp_hub.mcp_hub import McpHub
from backend.src.core.event_bus.event_bus import EventBus
from backend.src.core.logging_service.logging_service import LoggingService
from backend.src.core.metric_collector.metric_collector import MetricCollector
from backend.src.core.optimization_oracle.optimization_oracle import OptimizationOracle
from backend.src.core.sandbox_api.sandbox_api import SandboxAPI # Import SandboxAPI client
from backend.src.db.database import create_db_and_tables # Import database table creation function
from prometheus_client import start_http_server # Import for exposing metrics


# --- Configuration Loading (Placeholder) ---
# TODO: Implement proper configuration loading (e.g., from config files, environment variables)
# For now, using placeholder values
DEFINITION_STATE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "app_definitions") # Path relative to project root
RUNTIME_STATE_CONFIG = {"host": "localhost", "port": 6379, "db": 0} # Placeholder Redis config
MCP_SETTINGS = {} # Placeholder MCP settings
# TODO: Add other configuration settings (e.g., sandbox image, network config)


# --- Instantiate Core Components ---
# Instantiate lower-level services first, then those that depend on them.
# This order reflects the dependency graph.

# Foundational Services
event_bus_instance = EventBus()
logging_service_instance = LoggingService()
metric_collector_instance = MetricCollector()
mcp_hub_instance = McpHub(settings=MCP_SETTINGS) # MCP Hub needs settings
sandbox_api_instance = SandboxAPI() # SandboxAPI client (no dependencies in __init__)

# State Management
state_manager_instance = StateManager(
    definition_state_path=DEFINITION_STATE_PATH,
    runtime_state_config=RUNTIME_STATE_CONFIG
) # State Manager needs paths/config

# Services depending on StateManager, LoggingService, MetricCollector, McpHub, etc.
app_registry_instance = ApplicationRegistry(state_manager=state_manager_instance) # Application Registry needs State Manager
tool_manager_instance = ToolManager(app_registry=app_registry_instance, mcp_hub=mcp_hub_instance) # Tool Manager needs App Registry, MCP Hub
sandbox_manager_instance = SandboxManager(app_registry=app_registry_instance) # Sandbox Manager needs Application Registry
optimization_oracle_instance = OptimizationOracle(
    metric_collector=metric_collector_instance,
    state_manager=state_manager_instance
    # TODO: Optimization Oracle also needs ToolManager and potentially a JIT service - update __init__ and pass
)

# Request Router (depends on many other services)
request_router_instance = RequestRouter(
    app_registry=app_registry_instance,
    sandbox_manager=sandbox_manager_instance,
    sandbox_api=sandbox_api_instance, # Pass the SandboxAPI client instance
    tool_manager=tool_manager_instance,
    event_bus=event_bus_instance, # Pass EventBus instance
    logging_service=logging_service_instance,
    metric_collector=metric_collector_instance,
    # TODO: Request Router also needs AuthenticationService/AuthorizationService
)

# --- Wire Components (e.g., EventBus subscribers) ---
# Connect components that need to interact asynchronously via the EventBus
# Example: LoggingService might subscribe to events from EventBus
# event_bus_instance.subscribe("log_event", logging_service_instance.log_application_message) # Assuming log_event type and method name


# --- Pass instantiated services to FastAPI app dependencies ---
# The dependency provider functions in backend.src.api.main need to return these instances.
# Since they are currently defined globally in backend.src.api.main,
# this instantiation logic should ideally be moved there or managed by a DI container.
# For this POC main.py, we will rely on the global instances defined in api/main.py for now,
# but acknowledge this is not ideal wiring. The instantiation above serves as a demonstration
# of the required components and their dependencies.

# --- Main Execution Block ---
if __name__ == "__main__":
    print("Starting Nexus CoCreate AI Backend...")
    # TODO: Perform any necessary async startup initialization here
    # Example: await state_manager_instance._initialize_definition_state() # If not done in __init__
    # Example: await mcp_hub_instance.connect_initial_servers() # If connect method exists

    # Create database tables
    create_db_and_tables()

    # Start Prometheus metrics server
    # TODO: Make port configurable (Issue #XX)
    metrics_port = 8001
    start_http_server(metrics_port)
    print(f"Prometheus metrics server started on port {metrics_port}")

    # Run the FastAPI application using uvicorn
    # The app instance is imported from backend.src.api.main
    uvicorn.run(
        "backend.src.api.main:app", # Module:variable
        host="0.0.0.0", # Listen on all interfaces
        port=8000, # Default FastAPI port
        reload=True # Enable auto-reloading for development
        # TODO: Configure logging, workers, etc. for production
    )
