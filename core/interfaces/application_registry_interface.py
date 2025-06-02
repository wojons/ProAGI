from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from core.shared.data_models import AppDefinition, ComponentDefinition # Assuming these are needed

class ApplicationRegistryInterface(ABC):
    """
    Abstract interface for managing UHLP application definitions and status.

    Provides methods for registering, updating, deregistering, listing,
    and retrieving details about applications.
    """

    @abstractmethod
    def register_application(self, app_definition: AppDefinition) -> bool:
        """
        Registers a new UHLP application with the framework.

        Args:
            app_definition: The full definition of the application.

        Returns:
            True if registration was successful, False otherwise.
        """
        pass

    @abstractmethod
    def deregister_application(self, app_id: str) -> bool:
        """
        Deactivates or removes an application from framework management.

        Args:
            app_id: The ID of the application to deregister.

        Returns:
            True if deregistration was successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_application_definition(self, app_id: str) -> Optional[AppDefinition]:
        """
        Retrieves the complete, current definition for a specific application.

        Args:
            app_id: The ID of the application.

        Returns:
            The AppDefinition object if found, None otherwise.
        """
        pass

    @abstractmethod
    def update_application_definition(self, app_definition: AppDefinition) -> bool:
        """
        Applies updates to an existing application's definition.

        Args:
            app_definition: The AppDefinition object containing the updated fields.

        Returns:
            True if the update was successful, False otherwise.
        """
        pass

    @abstractmethod
    def list_applications(self) -> List[str]:
        """
        Returns a list of IDs for all applications currently managed by the framework.

        Returns:
            A list of application IDs (strings).
        """
        pass

    @abstractmethod
    def get_application_status(self, app_id: str) -> str:
        """
        Retrieves the current runtime status of an application.

        Args:
            app_id: The ID of the application.

        Returns:
            A string indicating the application status (e.g., 'Active', 'Inactive', 'Error').
        """
        pass

    @abstractmethod
    def get_component_definition(self, app_id: str, component_id: str) -> Optional[ComponentDefinition]:
        """
        Retrieves the definition for a specific component within an application.

        Args:
            app_id: The ID of the application.
            component_id: The ID of the component.

        Returns:
            The ComponentDefinition object if found, None otherwise.
        """
        pass

    @abstractmethod
    def resolve_trigger_to_component(self, app_id: str, trigger_details: Dict[str, Any]) -> Optional[ComponentDefinition]:
        """
        Resolves incoming trigger details (e.g., HTTP route) to a specific component definition.

        Args:
            app_id: The ID of the application.
            trigger_details: A dictionary containing details about the trigger event.

        Returns:
            The matching ComponentDefinition if found, None otherwise.
        """
        pass

    # Optional: Add methods for security/permissions lookup if needed here or in a separate interface
    # @abstractmethod
    # def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
    #     """Validates an API key and returns associated app ID and permissions."""
    #     pass

    # @abstractmethod
    # def get_user_permissions_for_app(self, app_id: str, user_id: str) -> List[str]:
    #     """Retrieves permissions for a user within an application."""
    #     pass
