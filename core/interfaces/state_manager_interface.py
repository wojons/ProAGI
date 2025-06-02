from abc import ABC, abstractmethod
from typing import List, Optional, Union

class StateManagerInterface(ABC):
    """
    Abstract interface for managing application state within the UHLP framework.

    Provides methods for interacting with both definition (Git/YAML) and
    runtime (Redis) state.
    """

    # --- Definition State Methods (Git/YAML) ---

    @abstractmethod
    def get_definition_file_content(self, app_id: str, file_path: str, revision: Optional[str] = None) -> bytes:
        """
        Reads the content of a specific state file at a given revision.

        Args:
            app_id: The ID of the application.
            file_path: The path to the file relative to the application's state root.
            revision: The Git revision (commit hash, branch name, tag). Defaults to current.

        Returns:
            The content of the file as bytes.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the revision is invalid.
            IOError: If there is an error reading the file.
        """
        pass

    @abstractmethod
    def apply_definition_diff(self, app_id: str, file_path: str, diff_content: str, expected_base_revision: str, commit_message: str, author: Optional[str] = None) -> str:
        """
        Atomically applies a provided patch/diff to a state file.

        Ensures the diff applies against the expected base revision (optimistic concurrency).
        Commits the change to the application's Git repository.

        Args:
            app_id: The ID of the application.
            file_path: The path to the file relative to the application's state root.
            diff_content: The patch content in standard diff format.
            expected_base_revision: The Git revision the diff is based on.
            commit_message: The Git commit message for this change.
            author: Optional author string for the Git commit.

        Returns:
            The resulting Git revision (commit hash) after applying the diff.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the expected_base_revision is invalid or the diff is malformed.
            ConflictError: If the diff cannot be applied cleanly against the expected_base_revision.
            IOError: If there is an error interacting with the Git repository.
        """
        pass

    @abstractmethod
    def set_definition_file_content(self, app_id: str, file_path: str, content: bytes, commit_message: str, author: Optional[str] = None) -> str:
        """
        Overwrites or creates a state file with new content.

        Commits the change to the application's Git repository. Use with caution;
        apply_definition_diff is preferred for modifications.

        Args:
            app_id: The ID of the application.
            file_path: The path to the file relative to the application's state root.
            content: The new content of the file as bytes.
            commit_message: The Git commit message for this change.
            author: Optional author string for the Git commit.

        Returns:
            The resulting Git revision (commit hash) after setting the content.

        Raises:
            IOError: If there is an error interacting with the Git repository.
        """
        pass

    @abstractmethod
    def delete_definition_file(self, app_id: str, file_path: str, commit_message: str, author: Optional[str] = None) -> str:
        """
        Deletes a state file within the application's Git repository.

        Args:
            app_id: The ID of the application.
            file_path: The path to the file relative to the application's state root.
            commit_message: The Git commit message for this change.
            author: Optional author string for the Git commit.

        Returns:
            The resulting Git revision (commit hash) after deleting the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there is an error interacting with the Git repository.
        """
        pass

    @abstractmethod
    def list_definition_directory(self, app_id: str, dir_path: str, recursive: bool = False, revision: Optional[str] = None) -> List[str]:
        """
        Lists files and subdirectories within a directory in the state repository.

        Args:
            app_id: The ID of the application.
            dir_path: The path to the directory relative to the application's state root.
            recursive: Whether to list contents recursively.
            revision: The Git revision. Defaults to current.

        Returns:
            A list of file and directory paths within the specified directory.

        Raises:
            FileNotFoundError: If the directory does not exist.
            ValueError: If the revision is invalid.
            IOError: If there is an error interacting with the Git repository.
        """
        pass

    # --- Runtime State Methods (Redis) ---

    @abstractmethod
    def set_runtime_value(self, app_id: str, key: str, value: str, ttl_seconds: Optional[int] = None) -> bool:
        """
        Sets or updates a key-value pair in the runtime state.

        Args:
            app_id: The ID of the application.
            key: The key for the value.
            value: The value to store (as a string).
            ttl_seconds: Optional time-to-live in seconds.

        Returns:
            True if the operation was successful, False otherwise.

        Raises:
            IOError: If there is an error interacting with the runtime state store.
        """
        pass

    @abstractmethod
    def get_runtime_value(self, app_id: str, key: str) -> Optional[str]:
        """
        Retrieves a value by key from the runtime state.

        Args:
            app_id: The ID of the application.
            key: The key for the value.

        Returns:
            The value as a string if found, None otherwise.

        Raises:
            IOError: If there is an error interacting with the runtime state store.
        """
        pass

    @abstractmethod
    def delete_runtime_value(self, app_id: str, key: str) -> bool:
        """
        Deletes a key from the runtime state.

        Args:
            app_id: The ID of the application.
            key: The key to delete.

        Returns:
            True if the operation was successful, False otherwise.

        Raises:
            IOError: If there is an error interacting with the runtime state store.
        """
        pass

    # Optional: Add increment/decrement methods if needed
    # @abstractmethod
    # def increment_runtime_value(self, app_id: str, key: str, amount: int = 1) -> int:
    #     """Atomically increments a numerical value by the specified amount."""
    #     pass
