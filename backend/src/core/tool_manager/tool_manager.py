from typing import Optional, Dict, Any, List
# TODO: Import a library for caching if needed (e.g., functools.lru_cache) (Issue #XX)

# Import necessary data models from core.shared.data_models
from core.shared.data_models.data_models import (
    ToolDefinition, # Assuming ToolDefinition data model exists
    ToolCall, # Assuming ToolCall data model exists
    ToolResult, # Assuming ToolResult data model exists
    # Import other relevant data models as needed
)

from core.interfaces.tool_manager_interface import ToolManagerInterface
from core.interfaces.application_registry_interface import ApplicationRegistryInterface
from core.interfaces.mcp_hub_interface import McpHubInterface

class ToolManager(ToolManagerInterface):
    """
    Manages the discovery, registration, and execution of tools available to the framework
    and applications. Aggregates tools from the ApplicationRegistry (app-provided tools)
    and the McpHub (MCP server-provided tools).
    """
    def __init__(self, app_registry: ApplicationRegistryInterface, mcp_hub: McpHubInterface):
        """
        Initializes the ToolManager with references to the ApplicationRegistry and McpHub.

        Args:
            app_registry: An instance of ApplicationRegistryInterface to discover app-provided tools.
            mcp_hub: An instance of McpHubInterface to discover and execute tools from connected MCP servers.
        """
        self.app_registry = app_registry
        self.mcp_hub = mcp_hub
        # TODO: Initialize internal cache for tool definitions if needed for performance (Issue #XX)
        self._tool_definitions_cache: Dict[str, ToolDefinition] = {} # tool_name: ToolDefinition

    async def register_tool(self, tool_definition: ToolDefinition):
        """
        Registers a new tool definition.
        For POC, this might just update the internal cache.
        In a real system, this might be triggered by app registration or MCP server connection.

        Args:
            tool_definition: The ToolDefinition object to register.
        """
        print(f"Registering tool: {tool_definition.name}") # Basic logging
        self._tool_definitions_cache[tool_definition.name] = tool_definition
        # TODO: In a real system, this might involve persisting the tool definition (Issue #XX)
        # or notifying other components.

    async def deregister_tool(self, tool_name: str):
        """
        Deregisters a tool by name.
        For POC, removes from internal cache.

        Args:
            tool_name: The name of the tool to deregister.
        """
        print(f"Deregistering tool: {tool_name}") # Basic logging
        if tool_name in self._tool_definitions_cache:
            del self._tool_definitions_cache[tool_name]
            # TODO: In a real system, this might involve removing the persistent definition (Issue #XX)
            # or notifying other components.
        else:
            print(f"Warning: Tool '{tool_name}' not found in cache for deregistration.") # Basic logging

    async def get_tool_definition(self, tool_name: str) -> Optional[ToolDefinition]:
        """
        Retrieves the definition of a specific tool by name.
        Searches in internal cache, ApplicationRegistry, and McpHub in that order.

        Args:
            tool_name: The name of the tool to retrieve the definition for.

        Returns:
            The ToolDefinition object if found, otherwise None.
        """
        print(f"Attempting to get tool definition for: {tool_name}") # Basic logging
        # Search in internal cache first
        if tool_name in self._tool_definitions_cache:
            print(f"Tool definition found in cache for: {tool_name}") # Basic logging
            return self._tool_definitions_cache[tool_name]

        # Search in ApplicationRegistry (tools exposed by applications)
        # Assuming ApplicationRegistry has a method like list_all_exposed_tools() (Issue #XX)
        # app_tools_response = await self.app_registry.list_all_exposed_tools()
        # if app_tools_response.get("success") and app_tools_response.get("tools"):
        #     for tool_def_data in app_tools_response["tools"]:
        #         try:
        #             tool_def = ToolDefinition(**tool_def_data) # Assuming data matches model
        #             if tool_def.name == tool_name:
        #                 self._tool_definitions_cache[tool_name] = tool_def # Cache it
        #                 print(f"Tool definition found in ApplicationRegistry for: {tool_name}") # Basic logging
        #                 return tool_def
        #         except (TypeError, AttributeError) as e:
        #             print(f"Error parsing tool definition from AppRegistry: {e}") # Basic logging
        #             # TODO: Log this error properly (Issue #XX)

        # Search in McpHub (tools provided by MCP servers)
        # Assuming McpHub has methods like list_servers() and list_tools(server_name) (Issue #XX)
        try:
            mcp_servers_response = await self.mcp_hub.list_servers()
            if mcp_servers_response.get("success") and mcp_servers_response.get("servers"):
                for server_info in mcp_servers_response["servers"]: # Assuming server_info has a 'name' field
                    server_name = server_info.get("name")
                    if server_name:
                        mcp_tools_response = await self.mcp_hub.list_tools(server_name)
                        if mcp_tools_response.get("success") and mcp_tools_response.get("tools"):
                            for tool_def_data in mcp_tools_response["tools"]:
                                try:
                                    # Assuming tool_def_data from McpHub matches ToolDefinition structure
                                    tool_def = ToolDefinition(**tool_def_data) # Assuming data matches model
                                    if tool_def.name == tool_name:
                                        self._tool_definitions_cache[tool_name] = tool_def # Cache it
                                        print(f"Tool definition found in McpHub server '{server_name}' for: {tool_name}") # Basic logging
                                        return tool_def
                                except (TypeError, AttributeError) as e:
                                    print(f"Error parsing tool definition from McpHub server {server_name}: {e}") # Basic logging
                                    # TODO: Log this error properly (Issue #XX)
        except Exception as e:
            print(f"Error communicating with McpHub during tool lookup: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)


        print(f"Tool definition not found for tool: {tool_name}") # Basic logging
        return None # Tool not found


    async def list_tools(self) -> List[ToolDefinition]:
        """
        Lists all available tools from all sources (internal cache, applications, and MCP servers).
        Aggregates definitions, handling potential duplicates by tool name.

        Returns:
            A list of unique ToolDefinition objects.
        """
        print("Listing all available tools.") # Basic logging
        all_tools: Dict[str, ToolDefinition] = {} # Use a dict to handle potential duplicates by name

        # Add tools from internal cache
        all_tools.update(self._tool_definitions_cache)

        # TODO: Get tools from ApplicationRegistry (Issue #XX)
        # Assuming ApplicationRegistry has a method like list_all_exposed_tools()
        # app_tools_response = await self.app_registry.list_all_exposed_tools()
        # if app_tools_response.get("success") and app_tools_response.get("tools"):
        #     for tool_def_data in app_tools_response["tools"]:
        #         try:
        #             tool_def = ToolDefinition(**tool_def_data) # Assuming data matches model
        #             all_tools[tool_def.name] = tool_def # Add/overwrite
        #         except (TypeError, AttributeError) as e:
        #             print(f"Error parsing tool definition from AppRegistry: {e}") # Basic logging
        #             # TODO: Log this error properly (Issue #XX)

        # Get tools from McpHub
        # Assuming McpHub has methods like list_servers() and list_tools(server_name) (Issue #XX)
        try:
            mcp_servers_response = await self.mcp_hub.list_servers()
            if mcp_servers_response.get("success") and mcp_servers_response.get("servers"):
                for server_info in mcp_servers_response["servers"]: # Assuming server_info has a 'name' field
                    server_name = server_info.get("name")
                    if server_name:
                        mcp_tools_response = await self.mcp_hub.list_tools(server_name)
                        if mcp_tools_response.get("success") and mcp_tools_response.get("tools"):
                            for tool_def_data in mcp_tools_response["tools"]:
                                try:
                                    # Assuming tool_def_data from McpHub matches ToolDefinition structure
                                    tool_def = ToolDefinition(**tool_def_data) # Assuming data matches model
                                    all_tools[tool_def.name] = tool_def # Add/overwrite
                                except (TypeError, AttributeError) as e:
                                    print(f"Error parsing tool definition from McpHub server {server_name}: {e}") # Basic logging
                                    # TODO: Log this error properly (Issue #XX)
        except Exception as e:
            print(f"Error communicating with McpHub during tool listing: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)


        print(f"Found {len(all_tools)} unique tools.") # Basic logging
        return list(all_tools.values())


    async def execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """
        Executes a specific tool based on the provided ToolCall.
        Determines the tool's source (Application or MCP Server) and dispatches the call
        to the appropriate component (McpHub or SandboxAPI).

        Args:
            tool_call: The ToolCall object containing the tool name, arguments, and tool_use_id.

        Returns:
            A ToolResult object containing the result of the tool execution or an error.
        """
        print(f"Attempting to execute tool: {tool_call.tool_name} (Tool Use ID: {tool_call.tool_use_id})") # Basic logging
        # Lookup tool definition to find its source (appId or server_name)
        tool_def = await self.get_tool_definition(tool_call.tool_name)

        if not tool_def:
            print(f"Error: Tool '{tool_call.tool_name}' not found.") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            return ToolResult(tool_use_id=tool_call.tool_use_id, content=f"Error: Tool '{tool_call.tool_name}' not found.", is_error=True)

        # Dispatch based on tool source
        # Assuming ToolDefinition has a 'source' field which is a dict like {"type": "mcp_server", "name": "server_name"}
        source = tool_def.source # TODO: Verify field name in ToolDefinition model (Issue #XX)
        if source and source.get("type") == "mcp_server" and source.get("name"):
            server_name = source["name"]
            print(f"Dispatching tool '{tool_call.tool_name}' to MCP server '{server_name}'") # Basic logging
            try:
                # Assuming McpHub.execute_tool takes server_name and ToolCall and returns ToolResult
                mcp_result = await self.mcp_hub.execute_tool(server_name, tool_call)
                print(f"Received result from MCP server '{server_name}' for tool '{tool_call.tool_name}' (Tool Use ID: {tool_call.tool_use_id})") # Basic logging
                return mcp_result # Assuming McpHub.execute_tool returns a ToolResult

            except Exception as e:
                print(f"Error executing MCP tool '{tool_call.tool_name}' on server '{server_name}': {e}") # Basic logging
                # TODO: Log this error properly (Issue #XX)
                return ToolResult(tool_use_id=tool_call.tool_use_id, content=f"Error executing MCP tool: {e}", is_error=True)

        elif source and source.get("type") == "app" and source.get("appId"):
            app_id = source["appId"]
            print(f"Dispatching tool '{tool_call.tool_name}' to application '{app_id}' sandbox") # Basic logging
            # TODO: Implement dispatching to an application sandbox to execute a tool (Issue #XX)
            # This would likely involve:
            # 1. Allocating/getting a sandbox for the app via SandboxManager
            # 2. Sending a request to the sandbox's internal API (SandboxAPI) to execute the tool
            # This interaction needs clarification in the specification.
            print(f"Warning: Execution of application-provided tools is not yet implemented in POC.") # Basic logging
            # Placeholder for application tool execution
            result_content = f"Placeholder: Executed application tool '{tool_call.tool_name}' for app '{app_id}' with args {tool_call.arguments}"
            return ToolResult(tool_use_id=tool_call.tool_use_id, content=result_content, is_error=False) # Or is_error=True? Depends on desired POC behavior

        else:
            print(f"Error: Tool '{tool_call.tool_name}' has an invalid or unsupported source type.") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            return ToolResult(tool_use_id=tool_call.tool_use_id, content=f"Error: Tool '{tool_call.tool_name}' has an invalid source.", is_error=True)

    # TODO: Add internal methods for caching tool definitions (Issue #XX)
    # TODO: Add internal methods for resolving tool sources (Issue #XX)
