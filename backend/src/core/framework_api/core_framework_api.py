from typing import Optional, Dict, Any
from datetime import datetime # Needed for placeholder log message
# TODO: Import a library for parsing/validating data models (e.g., Pydantic) (Issue #XX)

# Import necessary data models from core.shared.data_models
from core.shared.data_models.data_models import (
    LogMessage, # Assuming LogMessage data model exists (Issue #XX)
    Metric, # Assuming Metric data model exists (Issue #XX)
    ToolCall, # Assuming ToolCall data model exists (Issue #XX)
    ToolResult, # Assuming ToolResult data model exists (Issue #XX)
    Event, # Assuming Event data model exists (Issue #XX)
    # Import data models for state access if needed (e.g., FileInfo) (Issue #XX)
)

from core.interfaces.core_framework_api_interface import CoreFrameworkAPIInterface
# Import interfaces for components CoreFrameworkAPI interacts with
from core.interfaces.logging_service_interface import LoggingServiceInterface
from core.interfaces.metric_collector_interface import MetricCollectorInterface
from core.interfaces.application_registry_interface import ApplicationRegistryInterface
from core.interfaces.state_manager_interface import StateManagerInterface # Add StateManagerInterface dependency
from core.interfaces.tool_manager_interface import ToolManagerInterface # Add ToolManagerInterface dependency
from core.interfaces.event_bus_interface import EventBusInterface # Add EventBusInterface dependency


class CoreFrameworkAPI(CoreFrameworkAPIInterface):
    """
    Provides a gRPC-based API for application sandboxes to interact with core framework services.
    This allows sandboxes to log messages, record metrics, access configuration, manage state,
    execute tools, and publish events back to the Core Framework.
    """
    def __init__(
        self,
        logging_service: LoggingServiceInterface,
        metric_collector: MetricCollectorInterface,
        app_registry: ApplicationRegistryInterface,
        state_manager: StateManagerInterface,
        tool_manager: ToolManagerInterface, # Add ToolManagerInterface dependency
        event_bus: EventBusInterface, # Add EventBusInterface dependency
        # TODO: Add other core service interfaces if sandboxes need to interact with them (Issue #XX)
    ):
        """
        Initializes the CoreFrameworkAPI with references to other core components.

        Args:
            logging_service: Instance of LoggingService for handling logs from sandboxes.
            metric_collector: Instance of MetricCollector for handling metrics from sandboxes.
            app_registry: Instance of ApplicationRegistry for accessing application configuration.
            state_manager: Instance of StateManager for accessing application state.
            tool_manager: Instance of ToolManager for executing tools requested by sandboxes.
            event_bus: Instance of EventBus for publishing events from sandboxes.
        """
        self.logging_service = logging_service
        self.metric_collector = metric_collector
        self.app_registry = app_registry
        self.state_manager = state_manager
        self.tool_manager = tool_manager # Store reference to ToolManager
        self.event_bus = event_bus # Store reference to EventBus
        print("CoreFrameworkAPI initialized.") # Basic logging

    async def log_framework_message(self, log_message: LogMessage): # TODO: Define gRPC method signature (Issue #XX)
        """
        Logs a structured message originating from the Core Framework components.
        This method is exposed via gRPC for sandboxes to call back into the framework's logger.

        Args:
            log_message: The LogMessage object received from the sandbox.
        """
        print(f"CoreFrameworkAPI received framework log: {log_message.message}") # Basic logging
        await self.logging_service.log_framework_message(
            level=log_message.level,
            message=log_message.message,
            component_name=log_message.component_name,
            traceId=log_message.traceId,
            appId=log_message.appId,
            requestId=log_message.requestId,
            metadata=log_message.metadata
        )
        # TODO: Return a gRPC response (e.g., Empty or status) (Issue #XX)


    async def record_metric(self, metric: Metric): # TODO: Define gRPC method signature (Issue #XX)
        """
        Records a metric received from an application sandbox via the MetricCollector.

        Args:
            metric: The Metric object received from the sandbox.
                    Assumes Metric data model includes type (counter, gauge, histogram),
                    name, value (for gauge/histogram), and labels.
        """
        print(f"CoreFrameworkAPI received metric: {metric.name} (Type: {metric.type})") # Basic logging
        # TODO: Implement logic based on Metric type once data model is fully defined (Issue #XX)
        try:
            if metric.type == "counter":
                await self.metric_collector.increment_counter(metric.name, metric.labels)
            elif metric.type == "gauge":
                 # Assuming Metric has a 'value' field for Gauge
                if metric.value is not None:
                    await self.metric_collector.set_gauge(metric.name, metric.value, metric.labels)
                else:
                     await self.logging_service.log_framework_message(
                        level="warn",
                        message=f"Received gauge metric '{metric.name}' with no value.",
                        component_name="CoreFrameworkAPI",
                        appId=metric.appId, # Assuming appId is in Metric data model
                        traceId=metric.traceId, # Assuming traceId is in Metric data model
                        requestId=metric.requestId, # Assuming requestId is in Metric data model
                        # timestamp=datetime.now().isoformat(), # Handled by LoggingService
                        metadata={"metric_name": metric.name, "metric_type": metric.type}
                    )
            elif metric.type == "histogram":
                 # Assuming Metric has a 'value' field for Histogram
                if metric.value is not None:
                    await self.metric_collector.observe_histogram(metric.name, metric.value, metric.labels)
                else:
                     await self.logging_service.log_framework_message(
                        level="warn",
                        message=f"Received histogram metric '{metric.name}' with no value.",
                        component_name="CoreFrameworkAPI",
                        appId=metric.appId, # Assuming appId is in Metric data model
                        traceId=metric.traceId, # Assuming traceId is in Metric data model
                        requestId=metric.requestId, # Assuming requestId is in Metric data model
                        # timestamp=datetime.now().isoformat(), # Handled by LoggingService
                        metadata={"metric_name": metric.name, "metric_type": metric.type}
                    )
            else:
                # Log a warning if metric type is unknown
                await self.logging_service.log_framework_message(
                    level="warn",
                    message=f"Received metric with unknown type: {metric.type}",
                    component_name="CoreFrameworkAPI",
                    appId=metric.appId, # Assuming appId is in Metric data model
                    traceId=metric.traceId, # Assuming traceId is in Metric data model
                    requestId=metric.requestId, # Assuming requestId is in Metric data model
                    # timestamp=datetime.now().isoformat(), # Handled by LoggingService
                    metadata={"metric_name": metric.name, "metric_type": metric.type}
                )
        except Exception as e:
            print(f"Error recording metric {metric.name}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)

        # TODO: Return a gRPC response (e.g., Empty or status) (Issue #XX)


    async def get_config_value(self, appId: str, key: str, componentId: Optional[str] = None) -> Any: # TODO: Define gRPC method signature and return type (Issue #XX)
        """
        Retrieves a specific configuration value for an application or component from the ApplicationRegistry.
        This method is exposed via gRPC for sandboxes to access configuration.

        Args:
            appId: The ID of the application.
            key: The configuration key to retrieve.
            componentId: Optional ID of the component if retrieving component-specific config.

        Returns:
            The configuration value, or None/error if not found or an error occurs.
        """
        print(f"CoreFrameworkAPI received request for config key '{key}' for app '{appId}' (component: {componentId}).") # Basic logging
        # This calls the ApplicationRegistry method which handles lookup logic
        config_response = await self.app_registry.get_app_configuration_value(appId, key, componentId)
        # Assuming the response structure from ApplicationRegistry.get_app_configuration_value is {"success": bool, "key": str, "value": Any, ...}
        if config_response.get("success"):
            value = config_response.get("value")
            print(f"CoreFrameworkAPI returning config value for key '{key}': {value}") # Basic logging
            return value # TODO: Return value in a gRPC response object (Issue #XX)
        else:
            # TODO: Log a warning or error if config retrieval failed (Issue #XX)
            await self.logging_service.log_framework_message(
                level="warn",
                message=f"Failed to retrieve config key '{key}' for app '{appId}' (component: {componentId}).",
                component_name="CoreFrameworkAPI",
                appId=appId,
                traceId=None, # Trace/Request ID might not be available in this context
                requestId=None,
                # timestamp=datetime.now().isoformat(), # Handled by LoggingService
                metadata={"config_key": key, "component_id": componentId, "error": config_response.get("message")}
            )
            print(f"CoreFrameworkAPI failed to retrieve config key '{key}'.") # Basic logging
            return None # Return None or raise a gRPC exception if config is mandatory (Issue #XX)

    async def get_runtime_state(self, appId: str, key: str) -> Optional[Any]: # TODO: Define gRPC method signature and return type (Issue #XX)
        """
        Retrieves a runtime state value for an application from the StateManager.
        Exposed via gRPC for sandboxes to access volatile state.

        Args:
            appId: The ID of the application.
            key: The key for the runtime value.

        Returns:
            The runtime value, or None/error if not found or an error occurs.
        """
        print(f"CoreFrameworkAPI received request for runtime state key '{key}' for app '{appId}'.") # Basic logging
        try:
            value = await self.state_manager.get_runtime_value(appId, key)
            print(f"CoreFrameworkAPI returning runtime state value for key '{key}': {value}") # Basic logging
            return value # TODO: Return value in a gRPC response object (Issue #XX)
        except Exception as e:
            print(f"Error getting runtime state key '{key}' for app '{appId}': {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            # TODO: Return a gRPC error response (Issue #XX)
            return None # Or raise gRPC exception


    async def set_runtime_state(self, appId: str, key: str, value: Any): # TODO: Define gRPC method signature (Issue #XX)
        """
        Sets a runtime state value for an application via the StateManager.
        Exposed via gRPC for sandboxes to update volatile state.

        Args:
            appId: The ID of the application.
            key: The key for the runtime value.
            value: The value to set.
        """
        print(f"CoreFrameworkAPI received request to set runtime state key '{key}' for app '{appId}'.") # Basic logging
        try:
            await self.state_manager.set_runtime_value(appId, key, value)
            print(f"CoreFrameworkAPI successfully set runtime state key '{key}'.") # Basic logging
            # TODO: Return a gRPC response (e.g., Empty or status) (Issue #XX)
        except Exception as e:
            print(f"Error setting runtime state key '{key}' for app '{appId}': {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            # TODO: Return a gRPC error response (Issue #XX)


    async def delete_runtime_state(self, appId: str, key: str): # TODO: Define gRPC method signature (Issue #XX)
        """
        Deletes a runtime state value for an application via the StateManager.
        Exposed via gRPC for sandboxes to delete volatile state.

        Args:
            appId: The ID of the application.
            key: The key for the runtime value to delete.
        """
        print(f"CoreFrameworkAPI received request to delete runtime state key '{key}' for app '{appId}'.") # Basic logging
        try:
            await self.state_manager.delete_runtime_value(appId, key)
            print(f"CoreFrameworkAPI successfully deleted runtime state key '{key}'.") # Basic logging
            # TODO: Return a gRPC response (e.g., Empty or status) (Issue #XX)
        except Exception as e:
            print(f"Error deleting runtime state key '{key}' for app '{appId}': {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            # TODO: Return a gRPC error response (Issue #XX)


    async def get_definition_file(self, appId: str, path: str) -> Optional[str]: # TODO: Define gRPC method signature and return type (Issue #XX)
        """
        Retrieves the content of a definition file for an application from the StateManager.
        Exposed via gRPC for sandboxes to access definition/config files.

        Args:
            appId: The ID of the application.
            path: The path to the file relative to the application's definition root.

        Returns:
            The content of the file as a string, or None/error if not found or an error occurs.
        """
        print(f"CoreFrameworkAPI received request for definition file '{path}' for app '{appId}'.") # Basic logging
        try:
            content = await self.state_manager.get_definition_file_content(appId, path)
            print(f"CoreFrameworkAPI returning definition file content for '{path}'.") # Basic logging
            return content # TODO: Return content in a gRPC response object (Issue #XX)
        except Exception as e:
            print(f"Error getting definition file '{path}' for app '{appId}': {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            # TODO: Return a gRPC error response (Issue #XX)
            return None # Or raise gRPC exception


    async def execute_tool(self, tool_call: ToolCall) -> ToolResult: # TODO: Define gRPC method signature (Issue #XX)
        """
        Executes a tool requested by a sandbox via the ToolManager.
        Exposed via gRPC for sandboxes to perform tool calls.

        Args:
            tool_call: The ToolCall object received from the sandbox.

        Returns:
            A ToolResult object containing the result of the tool execution or an error.
        """
        print(f"CoreFrameworkAPI received request to execute tool '{tool_call.tool_name}' (Tool Use ID: {tool_call.tool_use_id}).") # Basic logging
        try:
            result = await self.tool_manager.execute_tool(tool_call)
            print(f"CoreFrameworkAPI returning tool execution result for '{tool_call.tool_name}'.") # Basic logging
            return result # Assuming ToolManager.execute_tool returns a ToolResult
        except Exception as e:
            print(f"Error executing tool '{tool_call.tool_name}': {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            # TODO: Return a gRPC error ToolResult (Issue #XX)
            return ToolResult(tool_use_id=tool_call.tool_use_id, content=f"Error executing tool: {e}", is_error=True)


    async def publish_event(self, event: Event): # TODO: Define gRPC method signature (Issue #XX)
        """
        Publishes an event received from a sandbox via the EventBus.
        Exposed via gRPC for sandboxes to publish events.

        Args:
            event: The Event object received from the sandbox.
        """
        print(f"CoreFrameworkAPI received request to publish event: {event.event_type}.") # Basic logging
        try:
            await self.event_bus.publish(event)
            print(f"CoreFrameworkAPI successfully published event: {event.event_type}.") # Basic logging
            # TODO: Return a gRPC response (e.g., Empty or status) (Issue #XX)
        except Exception as e:
            print(f"Error publishing event {event.event_type}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            # TODO: Return a gRPC error response (Issue #XX)


    # TODO: Add internal methods for interacting with core services (Issue #XX)
    # TODO: Implement the actual gRPC server logic to expose these methods (Issue #XX)
    # This would involve using grpcio.aio.server and adding the generated service to it.
