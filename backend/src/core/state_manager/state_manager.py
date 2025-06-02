from typing import Optional, Dict, Any, List
from typing import Optional, Dict, Any, List
import os
import git
import yaml
import redis
import subprocess # Import subprocess for git apply

from core.interfaces.state_manager_interface import StateManagerInterface
from core.shared.data_models.data_models import FileInfo # Assuming FileInfo data model exists

class StateManager(StateManagerInterface):
    """
    Manages application state, abstracting access to Definition/Config (Git/YAML) and Runtime (Redis) state stores.
    This component is critical for persisting application definitions, configurations, and runtime data.
    """
    def __init__(self, definition_state_path: str, runtime_state_config: dict):
        """
        Initializes the StateManager.

        Args:
            definition_state_path: The absolute path to the root directory where application definition state Git repositories will be stored.
                                   Each application will have its own subdirectory within this path, initialized as a Git repository.
            runtime_state_config: A dictionary containing configuration parameters for connecting to the Redis instance used for runtime state.
        """
        self.definition_state_path = definition_state_path
        self.runtime_state_config = runtime_state_config
        self._redis_client: Optional[redis.Redis] = None
        # The main StateManager instance doesn't hold a single repo reference,
        # as each app has its own repo. Repo instances are managed per-app as needed.
        # self._repo: Optional[git.Repo] = None # Removed as it's per-app

        self._initialize_definition_state_root() # Initialize the root directory
        self._initialize_runtime_state()

    def _initialize_definition_state_root(self):
        """Ensures the root directory for application definition state exists."""
        if not os.path.exists(self.definition_state_path):
            os.makedirs(self.definition_state_path)
            print(f"Created definition state root directory: {self.definition_state_path}")
        # Note: Individual application repositories are initialized when an app's state is first modified.


    def _initialize_runtime_state(self):
        """Initializes the Redis client for runtime state."""
        try:
            # Use connection_pool for better performance in async contexts if needed later
            # For POC, direct connection is fine.
            self._redis_client = redis.Redis(**self.runtime_state_config, decode_responses=True) # Decode responses to get strings
            # Ping to check connection
            self._redis_client.ping()
            print("Redis client initialized and connected.")
        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")
            self._redis_client = None # Ensure client is None if connection fails
            # TODO: Implement proper error handling or retry mechanism (Issue #XX)

    def _get_app_definition_path(self, app_id: str, path: str) -> str:
        """
        Gets the absolute path for an app's definition file or directory within its Git repository.

        Args:
            app_id: The ID of the application.
            path: The path relative to the application's definition root (e.g., 'config/app.yaml', 'workflows/my_workflow.yaml').

        Returns:
            The absolute path on the filesystem.

        Raises:
            ValueError: If the provided path attempts to escape the application's directory.
        """
        # Ensure path is relative and safe
        relative_path = os.path.normpath(path)
        if relative_path.startswith('..'):
             raise ValueError("Path cannot be outside the application's directory")
        # Construct the full path within the definition state repo
        full_path = os.path.join(self.definition_state_path, app_id, relative_path)
        return full_path

    def _get_app_runtime_key(self, app_id: str, key: str) -> str:
        """
        Gets the namespaced key for an app's runtime state in Redis.

        Args:
            app_id: The ID of the application.
            key: The key for the runtime value.

        Returns:
            The namespaced key (e.g., 'app_id:key').
        """
        # Simple namespacing: app_id:key
        return f"{app_id}:{key}"

    def _get_app_repo(self, app_id: str) -> git.Repo:
        """
        Gets the Git repository instance for a specific application.
        Initializes the repository if it doesn't exist.

        Args:
            app_id: The ID of the application.

        Returns:
            A GitPython Repo instance for the application's state repository.
        """
        app_repo_path = os.path.join(self.definition_state_path, app_id)
        if not os.path.exists(app_repo_path):
            os.makedirs(app_repo_path)
            repo = git.Repo.init(app_repo_path)
            # Initial commit with .gitignore
            gitignore_path = os.path.join(app_repo_path, '.gitignore')
            with open(gitignore_path, 'w') as f:
                f.write("# Ignore runtime state files if they somehow end up here\n")
                f.write("runtime/*\n") # Example ignore
            repo.index.add(['.gitignore'])
            repo.index.commit(f"Initial commit for application {app_id} definition state")
            print(f"Initialized Git repository for application: {app_id} at {app_repo_path}")
            return repo
        else:
            try:
                repo = git.Repo(app_repo_path)
                return repo
            except git.exc.InvalidGitRepositoryError:
                # If directory exists but is not a Git repo, this is an error state for this design.
                # It implies the directory was created outside the StateManager's control.
                # For POC, we'll raise an error. A robust system might attempt recovery.
                raise git.exc.InvalidGitRepositoryError(f"Directory exists but is not a Git repository: {app_repo_path}")
            except Exception as e:
                 print(f"Error accessing Git repository for {app_id}: {e}")
                 # TODO: Log this error properly (Issue #XX)
                 raise # Re-raise the exception


    async def get_definition_file_content(self, app_id: str, path: str) -> Optional[str]:
        """
        Retrieves the content of a definition file for a specific application.
        This is used to read application configurations, workflows, prompts, etc.

        Args:
            app_id: The ID of the application.
            path: The path to the file relative to the application's definition root (e.g., 'config/app.yaml').

        Returns:
            The content of the file as a string, or None if the file does not exist.
        """
        full_path = self._get_app_definition_path(app_id, path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f: # Specify encoding
                    return f.read()
            except Exception as e:
                print(f"Error reading definition file {full_path}: {e}")
                # TODO: Log this error properly (Issue #XX)
                return None # Return None on read error
        return None # Return None if file does not exist

    async def set_definition_file_content(self, app_id: str, path: str, content: str, message: str):
        """
        Sets the content of a definition file for a specific application and commits the change to Git.
        Creates the file and necessary directories if they don't exist.
        This is the primary method for modifying application definitions and configurations.

        Args:
            app_id: The ID of the application.
            path: The path to the file relative to the application's definition root.
            content: The content to write to the file.
            message: The Git commit message describing the change.
        """
        full_path = self._get_app_definition_path(app_id, path)
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}") # Log directory creation

        try:
            with open(full_path, 'w', encoding='utf-8') as f: # Specify encoding
                f.write(content)

            repo = self._get_app_repo(app_id) # Get or initialize the app's repo
            relative_repo_path = os.path.join(os.path.normpath(path)) # Path relative to app's repo root
            repo.index.add([relative_repo_path])
            repo.index.commit(message)
            print(f"Committed change to {relative_repo_path} for app {app_id} with message: '{message}'") # Log commit
        except Exception as e:
            print(f"Error setting definition file content for {full_path}: {e}")
            # TODO: Implement proper error handling and potentially Git rollback (Issue #XX)
            raise # Re-raise the exception


    async def delete_definition_file(self, app_id: str, path: str, message: str):
        """
        Deletes a definition file for a specific application and commits the change to Git.

        Args:
            app_id: The ID of the application.
            path: The path to the file relative to the application's definition root.
            message: The Git commit message describing the deletion.
        """
        full_path = self._get_app_definition_path(app_id, path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            try:
                os.remove(full_path)
                repo = self._get_app_repo(app_id) # Get the app's repo
                relative_repo_path = os.path.join(os.path.normpath(path)) # Path relative to app's repo root
                repo.index.remove([relative_repo_path])
                repo.index.commit(message)
                print(f"Deleted and committed {relative_repo_path} for app {app_id} with message: '{message}'") # Log deletion
            except Exception as e:
                print(f"Error deleting definition file {full_path}: {e}")
                # TODO: Implement proper error handling and potentially Git rollback (Issue #XX)
                raise # Re-raise the exception
        else:
            print(f"Warning: File not found for deletion: {full_path}")
            # TODO: Log this warning properly (Issue #XX)


    async def list_definition_directory(self, app_id: str, path: str) -> List[FileInfo]:
        """
        Lists the contents of a directory within an application's definition state.
        This is used to browse application files (configs, workflows, prompts).

        Args:
            app_id: The ID of the application.
            path: The path to the directory relative to the application's definition root.

        Returns:
            A list of FileInfo objects for the contents of the directory.
        """
        full_path = self._get_app_definition_path(app_id, path)
        file_list: List[FileInfo] = []
        if os.path.exists(full_path) and os.path.isdir(full_path):
            try:
                for item_name in os.listdir(full_path):
                    item_path = os.path.join(full_path, item_name)
                    is_dir = os.path.isdir(item_path)
                    # Construct relative path for FileInfo
                    relative_item_path = os.path.join(os.path.normpath(path), item_name)
                    file_list.append(FileInfo(path=relative_item_path, is_directory=is_dir))
                return file_list
            except Exception as e:
                print(f"Error listing directory {full_path}: {e}")
                # TODO: Log this error properly (Issue #XX)
                return [] # Return empty list on error
        return [] # Return empty list if directory does not exist or is not a directory

    async def apply_definition_diff(self, app_id: str, diff: str, message: str):
        """
        Applies a Git-style diff to the definition state for a specific application and commits the change.
        This method allows applying patches to multiple files or complex changes atomically.
        NOTE: This implementation uses the `git apply` command via subprocess, which is basic
        and does not handle conflicts automatically. For POC purposes.

        Args:
            app_id: The ID of the application.
            diff: The Git-style diff content as a string.
            message: The Git commit message.

        Raises:
            subprocess.CalledProcessError: If the `git apply` command fails.
            Exception: For other unexpected errors.
        """
        app_repo_path = os.path.join(self.definition_state_path, app_id)
        if not os.path.exists(app_repo_path) or not os.path.isdir(app_repo_path):
             print(f"Error: Application directory not found for diff application: {app_repo_path}")
             # TODO: Log this error properly (Issue #XX)
             raise FileNotFoundError(f"Application directory not found: {app_repo_path}")

        try:
            # Use subprocess to run git apply
            # --whitespace=fix attempts to fix whitespace issues
            # - reads diff from stdin
            # cwd sets the working directory to the application's repo
            result = subprocess.run(
                ['git', 'apply', '--whitespace=fix', '-'],
                cwd=app_repo_path,
                input=diff.encode('utf-8'), # Provide diff content via stdin
                capture_output=True,
                text=True, # Capture output as text
                check=True # Raise CalledProcessError if command returns non-zero exit code
            )
            print(f"Diff applied successfully for app {app_id} with message: '{message}'")
            if result.stdout:
                print("git apply stdout:\n", result.stdout)
            if result.stderr:
                 # git apply often writes informational messages to stderr even on success
                 print("git apply stderr:\n", result.stderr)

            # Commit the changes after applying the diff
            repo = self._get_app_repo(app_id) # Get the app's repo
            repo.index.add(A=True) # Add all changed files (including new/deleted)
            repo.index.commit(message)
            print(f"Committed changes after diff for app {app_id} with message: '{message}'") # Log commit

        except subprocess.CalledProcessError as e:
            print(f"Error applying diff for app {app_id}: {e}")
            print("git apply stdout:\n", e.stdout)
            print("git apply stderr:\n", e.stderr)
            # TODO: Log this error properly (Issue #XX)
            # TODO: Consider Git reset/rollback on failure (Issue #XX)
            raise # Re-raise the exception
        except Exception as e:
            print(f"Unexpected error during diff application for app {app_id}: {e}")
            # TODO: Log this error properly (Issue #XX)
            raise # Re-raise the exception


    async def get_runtime_value(self, app_id: str, key: str) -> Optional[Any]:
        """
        Retrieves a runtime value for a specific application from Redis.
        This is used for ephemeral session data, temporary workflow state, etc.

        Args:
            app_id: The ID of the application.
            key: The key for the runtime value.

        Returns:
            The value associated with the key, deserialized from YAML, or None if the key does not exist.
        """
        if self._redis_client:
            namespaced_key = self._get_app_runtime_key(app_id, key)
            try:
                value = self._redis_client.get(namespaced_key)
                if value:
                    # Attempt to deserialize from YAML
                    return yaml.safe_load(value)
                return None # Return None if key does not exist
            except redis.exceptions.RedisError as e:
                print(f"Redis error getting runtime value for {namespaced_key}: {e}")
                # TODO: Log this error properly (Issue #XX)
                return None # Return None on Redis error
            except (yaml.YAMLError, UnicodeDecodeError) as e:
                 print(f"Deserialization error for runtime value {namespaced_key}: {e}")
                 # TODO: Log this error properly (Issue #XX)
                 # Decide whether to return raw value or None on deserialization error
                 # For now, return None to indicate failure to retrieve usable data.
                 return None
            except Exception as e:
                 print(f"Unexpected error getting runtime value for {namespaced_key}: {e}")
                 # TODO: Log this error properly (Issue #XX)
                 return None
        else:
            print("Warning: Redis client not initialized. Cannot get runtime value.")
            # TODO: Implement proper error handling (Issue #XX)
            return None

    async def set_runtime_value(self, app_id: str, key: str, value: Any):
        """
        Sets a runtime value for a specific application in Redis.
        Serializes the value to YAML before storing.

        Args:
            app_id: The ID of the application.
            key: The key for the runtime value.
            value: The value to set (can be any serializable Python object).
        """
        if self._redis_client:
            namespaced_key = self._get_app_runtime_key(app_id, key)
            try:
                # Serialize value to YAML before storing
                serialized_value = yaml.dump(value)
                self._redis_client.set(namespaced_key, serialized_value)
                # print(f"Set runtime value for {namespaced_key}") # Optional: Log set
            except redis.exceptions.RedisError as e:
                print(f"Redis error setting runtime value for {namespaced_key}: {e}")
                # TODO: Log this error properly (Issue #XX)
                raise # Re-raise the exception
            except Exception as e:
                print(f"Unexpected error setting runtime value for {namespaced_key}: {e}")
                # TODO: Log this error properly (Issue #XX)
                raise # Re-raise the exception
        else:
            print("Warning: Redis client not initialized. Cannot set runtime value.")
            # TODO: Implement proper error handling (Issue #XX)
            # Decide whether to raise error or just warn
            pass # For POC, just pass silently after warning

    async def delete_runtime_value(self, app_id: str, key: str):
        """
        Deletes a runtime value for a specific application from Redis.

        Args:
            app_id: The ID of the application.
            key: The key for the runtime value.
        """
        if self._redis_client:
            namespaced_key = self._get_app_runtime_key(app_id, key)
            try:
                self._redis_client.delete(namespaced_key)
                # print(f"Deleted runtime value for {namespaced_key}") # Optional: Log deletion
            except redis.exceptions.RedisError as e:
                print(f"Redis error deleting runtime value for {namespaced_key}: {e}")
                # TODO: Log this error properly (Issue #XX)
                raise # Re-raise the exception
            except Exception as e:
                print(f"Unexpected error deleting runtime value for {namespaced_key}: {e}")
                # TODO: Log this error properly (Issue #XX)
                raise # Re-raise the exception
        else:
            print("Warning: Redis client not initialized. Cannot delete runtime value.")
            # TODO: Implement proper error handling (Issue #XX)
            pass # For POC, just pass silently after warning
