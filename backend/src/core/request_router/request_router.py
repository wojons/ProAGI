from typing import Optional, Dict, Any, List
import httpx # Using httpx for making HTTP requests to sandboxes
import time # Import time for measuring duration
# TODO: Import a library for parsing/validating sandbox responses (e.g., Pydantic) (Issue #XX)

# Import necessary data models from core.shared.data_models
from core.shared.data_models.data_models import (
    RequestPayload,
    ResponsePayload,
    ToolCall,
    ToolResult,
    Event,
    LogMessage,
    SandboxExecuteRequest, # Import SandboxExecuteRequest
    # Import other relevant data models as needed
)

from core.interfaces.request_router_interface import RequestRouterInterface
from core.interfaces.application_registry_interface import ApplicationRegistryInterface
from core.interfaces.sandbox_manager_interface import SandboxManagerInterface
from core.interfaces.sandbox_api_interface import SandboxAPIInterface # Assuming SandboxAPIInterface exists for dispatching
from core.interfaces.tool_manager_interface import ToolManagerInterface
from core.interfaces.event_bus_interface import EventBusInterface
from core.interfaces.logging_service_interface import LoggingServiceInterface
from core.interfaces.metric_collector_interface import MetricCollectorInterface


class RequestRouter(RequestRouterInterface):
    """
    Routes incoming requests to the appropriate application component within a sandboxed environment.
    This component orchestrates the request flow, including authentication, authorization,
    sandbox allocation, dispatching the request to the sandbox's internal API,
    and processing the response, including handling tool calls, events, and logs.
    """
    def __init__(
        self,
        app_registry: ApplicationRegistryInterface,
        sandbox_manager: SandboxManagerInterface,
        sandbox_api: SandboxAPIInterface, # Assuming SandboxAPI is a service the router talks to, not just an interface *in* the sandbox
        tool_manager: ToolManagerInterface,
        event_bus: EventBusInterface,
        logging_service: LoggingServiceInterface,
        metric_collector: MetricCollectorInterface,
        # TODO: Add AuthenticationService/AuthorizationService if needed (Issue #XX)
    ):
        """
        Initializes the RequestRouter with references to other core components.

        Args:
            app_registry: Instance of ApplicationRegistryInterface for application metadata.
            sandbox_manager: Instance of SandboxManagerInterface for managing sandbox lifecycles.
            sandbox_api: Instance of SandboxAPIInterface for dispatching requests to sandboxes.
            tool_manager: Instance of ToolManagerInterface for executing tool calls.
            event_bus: Instance of EventBusInterface for publishing events.
            logging_service: Instance of LoggingServiceInterface for logging.
            metric_collector: Instance of MetricCollectorInterface for metrics.
        """
        self.app_registry = app_registry
        self.sandbox_manager = sandbox_manager
        self.sandbox_api = sandbox_api # This might be an internal client to talk to sandboxes
        self.tool_manager = tool_manager
        self.event_bus = event_bus
        self.logging_service = logging_service
        self.metric_collector = metric_collector
        self._http_client = httpx.AsyncClient() # Async HTTP client for sandbox communication
        # TODO: Initialize AuthenticationService/AuthorizationService (Issue #XX)

    async def route_request(self, request: RequestPayload) -> ResponsePayload:
        """
        Routes an incoming request to the appropriate application component within a sandbox.
        This involves authenticating the request, allocating a sandbox, dispatching the
        request to the sandbox's internal /execute endpoint, and processing the response.

        Args:
            request: The incoming RequestPayload containing details about the request,
                     target application/component, and input data.

        Returns:
            The ResponsePayload from the application component execution, including
            the result, tool calls, events, and logs.
        """
        app_id = request.appId # Assuming appId is in RequestPayload
        request_id = request.requestId # Assuming requestId is in RequestPayload
        component_id = request.componentId # Assuming componentId is in RequestPayload
        input_data = request.inputData # Assuming inputData is in RequestPayload

        if not app_id or not component_id:
            print(f"Error: Invalid request payload. appId or componentId missing. Request ID: {request_id}")
            # TODO: Log this error properly (Issue #XX)
            # TODO: Return a proper error ResponsePayload (Issue #XX)
            return ResponsePayload(
                requestId=request_id,
                appId=app_id,
                success=False,
                message="Invalid request: appId or componentId missing."
            )

        print(f"Routing request for app '{app_id}', component '{component_id}', Request ID: {request_id}")
        await self.logging_service.log_framework_message(
             level="INFO",
             message=f"Routing request for app '{app_id}', component '{component_id}'",
             component_name="RequestRouter",
             traceId=request_id, # Using request_id as traceId for now
             appId=app_id,
             requestId=request_id
        )
        await self.metric_collector.increment_counter("request_router_requests_total", labels={"app_id": app_id, "component_id": component_id})

        # TODO: Authentication and Authorization (Placeholder for POC) (Issue #XX)
        # Validate API key/user and check permissions using ApplicationRegistry
        # auth_result = await self.app_registry.validate_api_key(request.apiKey) # Assuming apiKey is in RequestPayload
        # if not auth_result.get("success"):
        #     await self.logging_service.log_framework_message(...) # Log auth failure (Issue #XX)
        #     await self.metric_collector.increment_counter("request_router_auth_failures_total", labels={"app_id": app_id})
        #     return ResponsePayload(...) # Return auth error response (Issue #XX)

        try:
            # Get application and component definition
            app_details_response = await self.app_registry.get_application_details(app_id)
            if not app_details_response.get("success") or not app_details_response.get("definition"):
                print(f"Error: Could not get application details for app {app_id}. Request ID: {request_id}")
                # TODO: Log this error properly (Issue #XX)
                return ResponsePayload(
                    requestId=request_id,
                    appId=app_id,
                    success=False, # Use success field as per ResponsePayload
                    message="Application definition not found." # Use message field
                )
            app_definition = app_details_response["definition"]

            component_definition_response = await self.app_registry.get_component_definition(app_id, componentId=component_id)
            if not component_definition_response.get("success") or not component_definition_response.get("componentDefinition"):
                print(f"Error: Could not get component definition for app {app_id}, component {component_id}. Request ID: {request_id}")
                # TODO: Log this error properly (Issue #XX)
                return ResponsePayload(
                    requestId=request_id,
                    appId=app_id,
                    success=False,
                    message=f"Component '{component_id}' definition not found."
                )
            component_definition = component_definition_response["componentDefinition"]
            component_type = component_definition.type # Assuming ComponentDefinition has a 'type' field

            # Allocate a sandbox
            print(f"Attempting to allocate sandbox for app {app_id}. Request ID: {request_id}") # Basic logging
            allocate_response = await self.sandbox_manager.allocate_sandbox(app_id)
            if not allocate_response.get("success") or not allocate_response.get("sandboxId"):
                 print(f"Error: Could not allocate sandbox for app {app_id}. Request ID: {request_id}")
                 await self.logging_service.log_framework_message(
                      level="ERROR",
                      message=f"Could not allocate sandbox for app {app_id}",
                      component_name="RequestRouter",
                      traceId=request_id,
                      appId=app_id,
                      requestId=request_id
                 )
                 await self.metric_collector.increment_counter("request_router_sandbox_allocation_failures_total", labels={"app_id": app_id})
                 # TODO: Return a proper error ResponsePayload (Issue #XX)
                 return ResponsePayload(
                     requestId=request_id,
                     appId=app_id,
                     success=False,
                     message=allocate_response.get("message", "Failed to allocate sandbox.")
                 )

            sandbox_id = allocate_response["sandboxId"]
            # TODO: Get sandbox network address/endpoint from allocation response or SandboxManager (Issue #XX)

            # For POC, assume a fixed internal endpoint for the sandbox API
            # In a real implementation, this would be dynamic based on the allocated container's network config (Issue #XX)
            sandbox_api_url = f"http://localhost:8080/execute" # TODO: Replace with actual dynamic sandbox endpoint (Issue #XX)

            # Construct request for Sandbox API /execute endpoint
            sandbox_execute_payload = SandboxExecuteRequest(
                app_id=app_id,
                component_id=component_id,
                component_type=component_type, # Use component_type from definition
                component_definition=component_definition.definition, # Pass the actual definition
                input_data=input_data,
                tool_access_config=app_definition.config.get("tool_access_config", {}), # Example: Get from app config
                state_access_config=app_definition.config.get("state_access_config", {}), # Example: Get from app config
                request_id=request_id,
                # TODO: Populate task_id, trace_id if available (Issue #XX)
            )

            # Dispatch request to the sandbox's internal API
            print(f"Dispatching request to sandbox {sandbox_id} at {sandbox_api_url}. Request ID: {request_id}") # Basic logging
            await self.logging_service.log_framework_message(
                 level="INFO",
                 message=f"Dispatching request to sandbox {sandbox_id}",
                 component_name="RequestRouter",
                 traceId=request_id,
                 appId=app_id,
                 requestId=request_id,
                 metadata={"sandboxId": sandbox_id, "sandboxApiUrl": sandbox_api_url}
            )
            start_time = time.time() # For metrics

            try:
                # TODO: Use self.sandbox_api.execute_in_sandbox(sandbox_id, payload) if SandboxAPI is an internal service abstraction (Issue #XX)
                # For now, direct HTTP call for POC simplicity
                response = await self._http_client.post(sandbox_api_url, json=sandbox_execute_payload)
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                sandbox_response_data = response.json()
                # TODO: Validate sandbox_response_data against expected schema (e.g., using Pydantic) (Issue #XX)

                end_time = time.time()
                duration = end_time - start_time
                await self.metric_collector.observe_histogram("request_router_sandbox_execution_duration_seconds", duration, labels={"app_id": app_id, "component_id": component_id})
                await self.metric_collector.increment_counter("request_router_successful_requests_total", labels={"app_id": app_id, "component_id": component_id})

                print(f"Received response from sandbox {sandbox_id}. Request ID: {request_id}") # Basic logging

                # Process sandbox response
                final_result = sandbox_response_data.get("result") # Assuming 'result' field
                tool_calls: List[ToolCall] = [ToolCall(**tc) for tc in sandbox_response_data.get("toolCalls", [])] # Assuming 'toolCalls' field
                events: List[Event] = [Event(**e) for e in sandbox_response_data.get("events", [])] # Assuming 'events' field
                logs: List[LogMessage] = [LogMessage(**lm) for lm in sandbox_response_data.get("logs", [])] # Assuming 'logs' field
                # TODO: Handle metrics reported by the sandbox if any (Issue #XX)

                # Handle Tool Calls (Placeholder)
                for tool_call in tool_calls:
                    print(f"Processing Tool Call: {tool_call}") # Basic logging
                    # TODO: Use ToolManager to execute the tool call (Issue #XX)
                    # tool_result = await self.tool_manager.execute_tool(tool_call)
                    # TODO: Potentially send tool_result back to the sandbox or process further (Issue #XX)

                # Handle Events (Placeholder)
                for event in events:
                    print(f"Publishing Event: {event}") # Basic logging
                    # TODO: Use EventBus to publish the event (Issue #XX)
                    # await self.event_bus.publish(event)

                # Handle Logs (Placeholder)
                for log_message in logs:
                    print(f"Processing Log Message: {log_message}") # Basic logging
                    # TODO: Use LoggingService to process/store the log message (Issue #XX)
                    # await self.logging_service.log_framework_message(...) # Or a dedicated app log method

                # Construct final ResponsePayload
                response_payload = ResponsePayload(
                    requestId=request_id,
                    appId=app_id,
                    success=True, # Assuming sandbox execution was successful if no HTTP error
                    result=final_result,
                    toolCalls=tool_calls, # Include tool calls in the response? Or handle internally? (Issue #XX)
                    events=events, # Include events in the response? Or handle internally? (Issue #XX)
                    logs=logs, # Include logs in the response? Or handle internally? (Issue #XX)
                    # TODO: Add other relevant fields from sandbox response (Issue #XX)
                )
                print(f"Request processing complete for Request ID: {request_id}")
                await self.logging_service.log_framework_message(
                     level="INFO",
                     message=f"Request processing complete for app '{app_id}', component '{component_id}'",
                     component_name="RequestRouter",
                     traceId=request_id,
                     appId=app_id,
                     requestId=request_id,
                     metadata={"sandboxId": sandbox_id, "duration_seconds": duration}
                )
                return response_payload

            except httpx.HTTPStatusError as e:
                print(f"HTTP error dispatching to sandbox {sandbox_id}: {e}")
                await self.logging_service.log_framework_message(
                     level="ERROR",
                     message=f"HTTP error dispatching to sandbox {sandbox_id}: {e}",
                     component_name="RequestRouter",
                     traceId=request_id,
                     appId=app_id,
                     requestId=request_id,
                     metadata={"sandboxId": sandbox_id, "status_code": e.response.status_code}
                )
                await self.metric_collector.increment_counter("request_router_sandbox_http_errors_total", labels={"app_id": app_id, "component_id": component_id, "status_code": str(e.response.status_code)})
                # TODO: Release sandbox on error? (Issue #XX)
                # TODO: Return a proper error ResponsePayload (Issue #XX)
                return ResponsePayload(
                    requestId=request_id,
                    appId=app_id,
                    success=False,
                    message=f"Error communicating with sandbox: {e}"
                )
            except httpx.RequestError as e:
                 print(f"Request error dispatching to sandbox {sandbox_id}: {e}")
                 await self.logging_service.log_framework_message(
                      level="ERROR",
                      message=f"Request error dispatching to sandbox {sandbox_id}: {e}",
                      component_name="RequestRouter",
                      traceId=request_id,
                      appId=app_id,
                      requestId=request_id,
                      metadata={"sandboxId": sandbox_id}
                 )
                 await self.metric_collector.increment_counter("request_router_sandbox_request_errors_total", labels={"app_id": app_id, "component_id": component_id})
                 # TODO: Release sandbox on error? (Issue #XX)
                 # TODO: Return a proper error ResponsePayload (Issue #XX)
                 return ResponsePayload(
                     requestId=request_id,
                     appId=app_id,
                     success=False,
                     message=f"Error sending request to sandbox: {e}"
                 )
            except Exception as e:
                print(f"An unexpected error occurred during sandbox communication for sandbox {sandbox_id}: {e}")
                await self.logging_service.log_framework_message(
                     level="ERROR",
                     message=f"Unexpected error during sandbox communication for sandbox {sandbox_id}: {e}",
                     component_name="RequestRouter",
                     traceId=request_id,
                     appId=app_id,
                     requestId=request_id,
                     metadata={"sandboxId": sandbox_id}
                )
                await self.metric_collector.increment_counter("request_router_unexpected_errors_total", labels={"app_id": app_id, "component_id": component_id})
                # TODO: Release sandbox on error? (Issue #XX)
                # TODO: Return a proper error ResponsePayload (Issue #XX)
                return ResponsePayload(
                    requestId=request_id,
                    appId=app_id,
                    success=False,
                    message=f"An unexpected error occurred: {e}"
                )
            finally:
                 # TODO: Implement sandbox release/pooling logic here (Issue #XX)
                 # await self.sandbox_manager.release_sandbox(app_id, sandbox_id) # Release the sandbox if not pooled
                 pass # Add pass to satisfy expected indented block

        except Exception as e:
            print(f"An unexpected error occurred during request routing for app {app_id}, component {component_id}: {e}")
            await self.logging_service.log_framework_message(
                 level="ERROR",
                 message=f"Unexpected error during request routing for app {app_id}, component {component_id}: {e}",
                 component_name="RequestRouter",
                 traceId=request_id,
                 appId=app_id,
                 requestId=request_id
            )
            await self.metric_collector.increment_counter("request_router_unexpected_errors_total", labels={"app_id": app_id, "component_id": component_id})
            # TODO: Ensure any allocated sandboxes are cleaned up on error (Issue #XX)
            # TODO: Return a proper error ResponsePayload (Issue #XX)
            return ResponsePayload(
                requestId=request_id,
                appId=app_id,
                success=False,
                message=f"An unexpected error occurred during routing: {e}"
            )

    # TODO: Add internal methods for authentication, authorization, component lookup, sandbox allocation, and dispatching requests to sandboxes (Issue #XX)
