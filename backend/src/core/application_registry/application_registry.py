from typing import Optional, Dict, Any, List
import os
import yaml # Using PyYAML for parsing definition files
import bcrypt # Import bcrypt for hashing API keys
# TODO: Consider using json for some config files if needed

from sqlmodel import Session # Import Session for database interaction
from backend.src.db.models import ApiKey # Import the ApiKey model

# Import necessary data models from core.shared.data_models
from core.shared.data_models.data_models import (
    AppDefinition,
    AppStatus, # Assuming AppStatus enum/class is defined here or imported
    ComponentDefinition,
    SandboxPoolConfig,
    FileInfo,
    ToolDefinition,
    ResourceDefinition,
    InterAppPermission,
    UserPermissionsForApp,
    # Import other relevant data models as needed
)

from core.interfaces.application_registry_interface import ApplicationRegistryInterface
from core.interfaces.state_manager_interface import StateManagerInterface

# Define AppStatus enum if not already in data models (as per placeholder comment)
# Assuming AppStatus is an Enum or similar structure in data_models.py
# If not, define a simple class or Enum here for POC purposes.
# Example simple class (replace with actual import if available):
# class AppStatus:
#     UNSPECIFIED = "UNSPECIFIED"
#     ACTIVE = "ACTIVE"
#     INITIALIZING = "INITIALIZING"
#     INACTIVE = "INACTIVE"
#     DEGRADED = "DEGRADED"
#     ERROR = "ERROR"


class ApplicationRegistry(ApplicationRegistryInterface):
    """
    Manages application definitions, configurations, and lifecycle within the Nexus CoCreate AI framework.
    It acts as the central source of truth for registered applications and their metadata,
    interacting with the StateManager for persistent storage of AppDefinitions.
    """
    def __init__(self, state_manager: StateManagerInterface, db_session: Session):
        """
        Initializes the ApplicationRegistry.

        Args:
            state_manager: An instance of StateManagerInterface used to access application definition state.
            db_session: A database session instance.
        """
        self.state_manager = state_manager
        self.db_session = db_session
        # TODO: Initialize internal cache for AppDefinitions if needed for performance (Issue #XX)
        # self._app_definitions_cache: Dict[str, AppDefinition] = {}
        # TODO: Initialize internal state for tracking active applications (maybe a simple dict for POC) (Issue #XX)
        self._active_applications: Dict[str, AppStatus] = {} # Basic tracking for POC

    async def _get_app_definition(self, app_id: str) -> Optional[AppDefinition]:
        """
        Retrieves and parses the AppDefinition for a given app_id from the StateManager.

        Args:
            app_id: The ID of the application.

        Returns:
            The parsed AppDefinition object, or None if the definition file does not exist or parsing fails.
        """
        definition_content = await self.state_manager.get_definition_file_content(app_id, "app_definition.yaml")
        if definition_content:
            try:
                # Assuming app_definition.yaml contains the YAML representation of AppDefinition
                definition_data = yaml.safe_load(definition_content)
                # TODO: Add validation using Pydantic or similar if AppDefinition is a Pydantic model (Issue #XX)
                return AppDefinition(**definition_data)
            except (yaml.YAMLError, TypeError, AttributeError) as e:
                print(f"Error parsing AppDefinition for {app_id}: {e}")
                # TODO: Log this error properly (Issue #XX)
                return None
        return None

    async def _set_app_definition(self, app_id: str, definition: AppDefinition, message: str):
        """
        Serializes and saves the AppDefinition for a given app_id to the StateManager.

        Args:
            app_id: The ID of the application.
            definition: The AppDefinition object to save.
            message: The Git commit message for the StateManager operation.
        """
        try:
            # Assuming AppDefinition can be serialized to YAML
            definition_content = yaml.dump(definition.model_dump() if hasattr(definition, 'model_dump') else definition.__dict__) # Use model_dump for Pydantic v2+, __dict__ otherwise
            await self.state_manager.set_definition_file_content(app_id, "app_definition.yaml", definition_content, message)
            print(f"Saved AppDefinition for {app_id}") # Basic logging
        except Exception as e:
            print(f"Error saving AppDefinition for {app_id}: {e}")
            # TODO: Log this error properly (Issue #XX)
            raise # Re-raise the exception

    # Application Lifecycle & Management Methods
    async def register_application(self, definition: AppDefinition) -> Dict[str, Any]: # TODO: Return RegisterApplicationResponse (Issue #XX)
        """
        Registers a new application by saving its definition via the StateManager.
        Ensures the application ID is unique.

        Args:
            definition: The AppDefinition object for the new application.

        Returns:
            A dictionary indicating success/failure and potentially the assigned appId and initial status.
        """
        app_id = definition.appId # Assuming appId is part of AppDefinition
        if not app_id:
            # TODO: Generate a unique app_id if not provided (Issue #XX)
            print("Error: AppDefinition must contain appId.")
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": "AppId is required"}

        existing_definition = await self._get_app_definition(app_id)
        if existing_definition:
            print(f"Warning: Application with appId '{app_id}' already exists.")
            # TODO: Return a proper error response indicating conflict (Issue #XX)
            return {"success": False, "message": f"Application '{app_id}' already exists"}

        try:
            await self._set_app_definition(app_id, definition, f"Register application {app_id}")
            self._active_applications[app_id] = AppStatus.INITIALIZING # Basic status tracking for POC
            print(f"Application '{app_id}' registered successfully.") # Basic logging
            # TODO: Return a proper success response (RegisterApplicationResponse) (Issue #XX)
            return {"success": True, "appId": app_id, "status": AppStatus.INITIALIZING}
        except Exception as e:
            print(f"Error during application registration for {app_id}: {e}")
            # TODO: Log this error properly (Issue #XX)
            # TODO: Consider cleaning up partial state if save failed (Issue #XX)
            return {"success": False, "message": f"Failed to register application: {e}"}


    async def update_application(self, appId: str, update_mask: Optional[List[str]], updated_definition_fields: Dict[str, Any]) -> Dict[str, Any]: # TODO: Return UpdateApplicationResponse (Issue #XX)
        """
        Updates an existing application's definition by merging provided fields and saving via StateManager.
        NOTE: This is a simplified merge for POC. A robust implementation would use update_mask.

        Args:
            appId: The ID of the application to update.
            update_mask: Optional list of field paths to update (ignored in POC).
            updated_definition_fields: Dictionary of fields and values to update in the AppDefinition.

        Returns:
            A dictionary indicating success/failure.
        """
        existing_definition = await self._get_app_definition(appId)
        if not existing_definition:
            print(f"Error: Application with appId '{appId}' not found for update.")
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"Application '{appId}' not found"}

        # Simple merge logic for POC - update fields from updated_definition_fields
        # A more robust implementation would use update_mask and handle nested structures (Issue #XX)
        updated_definition_data = existing_definition.model_dump() if hasattr(existing_definition, 'model_dump') else existing_definition.__dict__
        updated_definition_data.update(updated_definition_fields)

        try:
            # Attempt to create a new AppDefinition instance to validate the updated data structure
            updated_definition = AppDefinition(**updated_definition_data)
            await self._set_app_definition(appId, updated_definition, f"Update application {appId}")
            print(f"Application '{appId}' updated successfully.") # Basic logging
            # TODO: Return a proper success response (UpdateApplicationResponse) (Issue #XX)
            return {"success": True, "appId": appId}
        except (TypeError, AttributeError) as e:
            print(f"Error creating updated AppDefinition for {appId}: {e}")
            # TODO: Log this error properly (Issue #XX)
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"Invalid update data: {e}"}
        except Exception as e:
            print(f"Error during application update for {appId}: {e}")
            # TODO: Log this error properly (Issue #XX)
            return {"success": False, "message": f"Failed to update application: {e}"}


    async def deregister_application(self, appId: str, deleteState: bool = False) -> Dict[str, Any]: # TODO: Return DeregisterApplicationResponse (Issue #XX)
        """
        Deregisters an application by removing its definition. Optionally deletes its definition state.

        Args:
            appId: The ID of the application to deregister.
            deleteState: If True, also deletes the application's definition state directory.

        Returns:
            A dictionary indicating success/failure.
        """
        existing_definition = await self._get_app_definition(appId)
        if not existing_definition:
            print(f"Warning: Application with appId '{appId}' not found for deregistration.")
            # TODO: Return a proper response indicating not found (Issue #XX)
            return {"success": False, "message": f"Application '{appId}' not found"}

        try:
            if deleteState:
                # TODO: Implement recursive deletion of the app's directory in definition state (Issue #XX)
                # For POC, just delete the main definition file
                await self.state_manager.delete_definition_file(appId, "app_definition.yaml", f"Deregister application {appId} and delete state")
                # TODO: Also delete runtime state associated with this app_id from Redis (Issue #XX)
                # This would require iterating keys or using Redis SCAN with the namespace prefix
                print(f"Definition state for '{appId}' deleted.")

            if appId in self._active_applications:
                del self._active_applications[appId] # Basic status tracking for POC

            print(f"Application '{appId}' deregistered successfully.") # Basic logging
            # TODO: Return a proper success response (DeregisterApplicationResponse) (Issue #XX)
            return {"success": True, "appId": appId}
        except Exception as e:
            print(f"Error during application deregistration for {appId}: {e}")
            # TODO: Log this error properly (Issue #XX)
            return {"success": False, "message": f"Failed to deregister application: {e}"}


    async def get_application_status(self, appId: str) -> Dict[str, Any]: # TODO: Return GetApplicationStatusResponse (Issue #XX)
        """
        Retrieves the current status of an application.
        For POC, returns basic internal status.

        Args:
            appId: The ID of the application.

        Returns:
            A dictionary containing the application ID and its status.
        """
        status = self._active_applications.get(appId, AppStatus.UNSPECIFIED)
        # TODO: In a real implementation, this would check sandbox status, health checks, etc. (Issue #XX)
        # TODO: Return a proper response (GetApplicationStatusResponse) including more details (Issue #XX)
        return {"appId": appId, "status": status}


    async def list_active_applications(self) -> Dict[str, Any]: # TODO: Return ListActiveApplicationsResponse (Issue #XX)
        """
        Lists all applications currently considered active by the registry.
        For POC, lists apps in the internal status tracking dict.

        Returns:
            A dictionary containing a list of active applications and their basic status.
        """
        # TODO: In a real implementation, this might involve querying the StateManager for all app directories
        # and checking their status, or relying on a more robust internal state. (Issue #XX)
        active_apps_list = [{"appId": appId, "status": status} for appId, status in self._active_applications.items()]
        # TODO: Return a proper response (ListActiveApplicationsResponse) (Issue #XX)
        return {"applications": active_apps_list}

    # Configuration & Requirements Retrieval Methods
    async def get_application_details(self, appId: str) -> Dict[str, Any]: # TODO: Return GetApplicationDetailsResponse (Issue #XX)
        """
        Retrieves the full definition details for an application from the StateManager.

        Args:
            appId: The ID of the application.

        Returns:
            A dictionary containing the application definition or an error message.
        """
        definition = await self._get_app_definition(appId)
        if not definition:
            print(f"Error: Application with appId '{appId}' not found for details.")
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"Application '{appId}' not found"}

        # TODO: Return a proper response (GetApplicationDetailsResponse) (Issue #XX)
        return {"success": True, "definition": definition}


    async def get_sandbox_requirements(self, appId: str) -> Dict[str, Any]: # TODO: Return GetSandboxRequirementsResponse (Issue #XX)
        """
        Retrieves the sandbox requirements for an application from its definition.

        Args:
            appId: The ID of the application.

        Returns:
            A dictionary containing the sandbox requirements or an error message.
        """
        definition = await self._get_app_definition(appId)
        if not definition:
            print(f"Error: Application with appId '{appId}' not found for sandbox requirements.")
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"Application '{appId}' not found"}

        # Assuming SandboxPoolConfig is part of AppDefinition
        # TODO: Verify field name in AppDefinition model (Issue #XX)
        sandbox_config = definition.sandboxPools
        if not sandbox_config:
             print(f"Warning: Sandbox requirements not found for application '{appId}'.")
             # TODO: Return a proper response indicating not found (Issue #XX)
             return {"success": False, "message": f"Sandbox requirements not found for application '{appId}'"}

        # TODO: Return a proper response (GetSandboxRequirementsResponse) (Issue #XX)
        return {"success": True, "sandboxRequirements": sandbox_config}


    async def get_component_definition(self, appId: str, componentId: Optional[str] = None, routeInput: Optional[Dict[str, Any]] = None) -> Dict[str, Any]: # TODO: Return GetComponentDefinitionResponse (Issue #XX)
        """
        Retrieves the definition for a specific component within an application.
        Component lookup might be based on componentId or input routing logic.
        For POC, assumes componentId is provided and looks it up in the ComponentRegistry.

        Args:
            appId: The ID of the application.
            componentId: The ID of the component to retrieve (for direct lookup).
            routeInput: Optional input data for routing logic (ignored in POC).

        Returns:
            A dictionary containing the component definition or an error message.
        """
        definition = await self._get_app_definition(appId)
        if not definition:
            print(f"Error: Application with appId '{appId}' not found for component definition.")
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"Application '{appId}' not found"}

        # Assuming ComponentRegistry is part of AppDefinition and is a dict/list of ComponentDefinition
        # TODO: Verify field name and structure in AppDefinition model (Issue #XX)
        component_registry = definition.components
        if not component_registry:
            print(f"Error: Component registry not found for application '{appId}'.")
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"Component registry not found for application '{appId}'"}

        # For POC, simple lookup by componentId
        if componentId and isinstance(component_registry, dict):
             component_def = component_registry.get(componentId)
             if component_def:
                 # TODO: Return a proper response (GetComponentDefinitionResponse) (Issue #XX)
                 return {"success": True, "componentDefinition": component_def}
             else:
                 print(f"Error: Component '{componentId}' not found in registry for application '{appId}'.")
                 # TODO: Return a proper error response (Issue #XX)
                 return {"success": False, "message": f"Component '{componentId}' not found"}
        # TODO: Implement logic for routing based on routeInput if componentId is None (Issue #XX)

        print(f"Error: Invalid request for component definition for application '{appId}'.")
        # TODO: Return a proper error response (Issue #XX)
        return {"success": False, "message": "Invalid request for component definition"}


    async def get_app_configuration_value(self, appId: str, key: str, componentId: Optional[str] = None) -> Dict[str, Any]: # TODO: Return GetAppConfigurationValueResponse (Issue #XX)
        """
        Retrieves a specific configuration value for an application or component from its definition.

        Args:
            appId: The ID of the application.
            key: The configuration key to retrieve.
            componentId: Optional ID of the component if retrieving component-specific config (ignored in POC).

        Returns:
            A dictionary containing the configuration key and value, or an error message.
        """
        definition = await self._get_app_definition(appId)
        if not definition:
            print(f"Error: Application with appId '{appId}' not found for configuration.")
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"Application '{appId}' not found"}

        # Assuming configuration is a dict within AppDefinition
        # TODO: Verify field name in AppDefinition model (Issue #XX)
        config = definition.config
        if not config:
            print(f"Warning: Configuration not found for application '{appId}'.")
            # TODO: Return a proper response indicating not found (Issue #XX)
            return {"success": False, "message": f"Configuration not found for application '{appId}'"}

        # For POC, simple lookup by key
        if key in config:
            value = config[key]
            # TODO: Handle component-specific config if componentId is provided (Issue #XX)
            # TODO: Return a proper response (GetAppConfigurationValueResponse) (Issue #XX)
            return {"success": True, "key": key, "value": value}
        else:
            print(f"Warning: Configuration key '{key}' not found for application '{appId}'.")
            # TODO: Return a proper response indicating not found (Issue #XX)
            return {"success": False, "message": f"Configuration key '{key}' not found for application '{appId}'"}

    # Security: Validation & Permissions Retrieval Methods
    async def validate_api_key(self, apiKey: str) -> Dict[str, Any]: # TODO: Return ValidateApiKeyResponse (Issue #XX)
        """
        Validates an API key against stored keys.
        For POC, this is a placeholder and does not perform actual validation.

        Args:
            apiKey: The API key to validate.

        Returns:
            A dictionary indicating success/failure and associated metadata (app, user, permissions) if valid.
        """
        print(f"Validating API key: {apiKey[:4]}...") # Log first few chars for security

        # TODO: Implement proper API key hashing and comparison (Issue #XX)
        # This requires retrieving the hashed key from the database based on some identifier.
        # For now, we'll query by the hashed key directly, which is NOT secure.
        # A proper implementation would involve a lookup table or a different key structure.
        # This is a temporary implementation for POC database integration.

        # Hash the incoming API key for comparison (temporary approach)
        # TODO: Refine this lookup strategy (Issue #XX)
        hashed_input_key = bcrypt.hashpw(apiKey.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') # This is just to match the 'hashed_key' field type

        # Query the database for an active API key matching the hashed key
        # TODO: This query is insecure as it relies on matching the hashed key directly.
        # A proper approach would be to lookup by a key ID or prefix and then compare hashes. (Issue #XX)
        statement = select(ApiKey).where(ApiKey.hashed_key == hashed_input_key, ApiKey.is_active == True)
        result = self.db_session.exec(statement).first()

        if result:
            print(f"API key validated successfully for app: {result.app_id}") # Basic logging
            # Return associated metadata
            permissions_list = result.permissions.split(',') if result.permissions else [] # Parse comma-separated permissions
            return {
                "success": True,
                "appId": result.app_id,
                "userId": result.user_id,
                "permissions": permissions_list
            }
        else:
            print(f"API key validation failed for key: {apiKey[:4]}...") # Log first few chars
            return {"success": False, "message": "Invalid or inactive API key"}


    async def get_application_permissions(self, appId: str) -> Dict[str, Any]: # TODO: Return GetApplicationPermissionsResponse (Issue #XX)
        """
        Retrieves the permissions defined for an application (e.g., inter-app permissions).
        For POC, this is a placeholder.

        Args:
            appId: The ID of the application.

        Returns:
            A dictionary containing the application's defined permissions.
        """
        print(f"Placeholder: Getting application permissions for {appId} (POC)")
        # TODO: Implement logic to retrieve InterAppPermissions from AppDefinition or a separate file (Issue #XX)
        # For POC, return empty or dummy data
        # Example placeholder:
        definition = await self._get_app_definition(appId)
        if definition and definition.permissions: # Assuming permissions field exists
            return {"success": True, "permissions": definition.permissions}
        else:
            return {"success": True, "permissions": []}


    async def get_user_permissions_for_app(self, appId: str, userId: str) -> Dict[str, Any]: # TODO: Return GetUserPermissionsForAppResponse (Issue #XX)
        """
        Retrieves the permissions a specific user has for an application.
        For POC, this is a placeholder.

        Args:
            appId: The ID of the application.
            userId: The ID of the user.

        Returns:
            A dictionary containing the user's permissions for the application.
        """
        print(f"Placeholder: Getting user {userId} permissions for app {appId} (POC)")
        # TODO: Implement logic to retrieve user-specific permissions (from StateManager/DB) (Issue #XX)
        # For POC, return empty or dummy data
        # Example placeholder:
        # if userId == "admin":
        #     return {"success": True, "userId": userId, "appId": appId, "permissions": ["read", "write", "manage"]}
        # else:
        #     return {"success": True, "userId": userId, "appId": appId, "permissions": ["read"]}
        return {"success": True, "userId": userId, "appId": appId, "permissions": []}

    # TODO: Add internal methods for interacting with StateManager to load/save definitions (Issue #XX)
    # TODO: Add internal methods for API key hashing and validation (Issue #XX)
    # TODO: Add internal methods for managing active application status (Issue #XX)
