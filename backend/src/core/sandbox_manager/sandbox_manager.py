from typing import Optional, Dict, Any, List
import docker
import docker.models.containers
import time # Import time for measuring duration
# TODO: Import necessary data models from core.shared.data_models (SandboxStatus, SandboxPoolConfig, AppDefinition) (Issue #XX)
from core.shared.data_models.data_models import (
    SandboxStatus, # Assuming SandboxStatus data model exists
    SandboxPoolConfig, # Assuming SandboxPoolConfig data model exists
    # AppDefinition # AppDefinition might be needed for requirements, but accessed via AppRegistry
)

from core.interfaces.sandbox_manager_interface import SandboxManagerInterface
from core.interfaces.application_registry_interface import ApplicationRegistryInterface

class SandboxManager(SandboxManagerInterface):
    """
    Manages the lifecycle and operations of application sandboxes, implemented as Docker containers.
    It interacts with the ApplicationRegistry to get sandbox requirements and uses the Docker SDK
    to create, start, stop, remove, and monitor containers.
    """
    def __init__(self, app_registry: ApplicationRegistryInterface):
        """
        Initializes the SandboxManager with a reference to the ApplicationRegistry and the Docker client.

        Args:
            app_registry: An instance of ApplicationRegistryInterface used to retrieve application-specific sandbox requirements.
        """
        self.app_registry = app_registry
        self._docker_client: Optional[docker.DockerClient] = None
        # TODO: Initialize internal state for managing sandbox pools and instances (Issue #XX)
        # self._sandbox_pools: Dict[str, SandboxPoolConfig] = {} # app_id: pool_config
        # self._sandbox_instances: Dict[str, List[docker.models.containers.Container]] = {} # app_id: list of container objects

        self._initialize_docker_client()

    def _initialize_docker_client(self):
        """Initializes the Docker client."""
        try:
            self._docker_client = docker.from_env()
            # Ping to check connection
            self._docker_client.ping()
            print("Docker client initialized and connected.") # Basic logging
        except docker.errors.DockerException as e:
            print(f"Error connecting to Docker: {e}") # Basic logging
            self._docker_client = None # Ensure client is None if connection fails
            # TODO: Implement proper error handling or retry mechanism (Issue #XX)

    async def _get_app_sandboxes(self, app_id: str) -> List[docker.models.containers.Container]:
        """
        Retrieves all Docker containers associated with a specific application using container labels.

        Args:
            app_id: The ID of the application.

        Returns:
            A list of Docker container objects.
        """
        if not self._docker_client:
            print("Warning: Docker client not initialized. Cannot list containers.") # Basic logging
            return []
        try:
            # Assuming containers are labeled with 'app_id'
            containers = self._docker_client.containers.list(all=True, filters={"label": f"app_id={app_id}"}) # Include stopped containers
            return containers
        except docker.errors.DockerException as e:
            print(f"Error listing Docker containers for app {app_id}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            return []

    async def allocate_sandbox(self, appId: str) -> Dict[str, Any]: # TODO: Return Sandbox instance/identifier (Issue #XX)
        """
        Allocates a sandbox (Docker container) for a specific application.
        This method should ideally allocate from a pool or create a new container
        based on the application's sandbox requirements.
        For POC, it creates and starts a single container.

        Args:
            appId: The ID of the application requiring a sandbox.

        Returns:
            A dictionary indicating success/failure and details about the allocated sandbox.
        """
        if not self._docker_client:
            print("Error: Docker client not initialized. Cannot allocate sandbox.") # Basic logging
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": "Docker client not initialized"}

        # Get sandbox requirements from Application Registry
        requirements_response = await self.app_registry.get_sandbox_requirements(appId)
        if not requirements_response.get("success") or not requirements_response.get("sandboxRequirements"):
            print(f"Error: Could not get sandbox requirements for app {appId}.") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"Could not get sandbox requirements for app {appId}"}

        sandbox_config: SandboxPoolConfig = requirements_response["sandboxRequirements"] # TODO: Ensure this matches the actual return type (Issue #XX)

        # For POC, create and start a single container
        try:
            # TODO: Implement pooling logic (allocate from pool or create new) (Issue #XX)
            # TODO: Configure resource limits, volumes, networking, etc. based on sandbox_config (Issue #XX)
            # TODO: Ensure the image exists (pull if necessary) (Issue #XX)
            image = sandbox_config.image # Assuming image is a field in SandboxPoolConfig
            if not image:
                 print(f"Error: Sandbox image not specified for app {appId}.") # Basic logging
                 # TODO: Return a proper error response (Issue #XX)
                 return {"success": False, "message": f"Sandbox image not specified for app {appId}"}

            print(f"Creating and starting sandbox container for app {appId} using image '{image}'.") # Basic logging
            container = self._docker_client.containers.run(
                image,
                detach=True, # Run in background
                labels={"app_id": appId}, # Label container with app_id
                # TODO: Add command/entrypoint based on sandbox type (JIT, LLM Orchestrator) (Issue #XX)
                # TODO: Mount volumes for definition state, logs, etc. (Issue #XX)
                # TODO: Configure networking (Issue #XX)
                # TODO: Set resource limits (CPU, memory) (Issue #XX)
            )
            print(f"Sandbox container created and started for app {appId}: {container.id}") # Basic logging
            # TODO: Return a proper response including sandbox identifier and network info (Issue #XX)
            return {"success": True, "sandboxId": container.id, "status": "running"} # TODO: Return a Sandbox instance/identifier object

        except docker.errors.ImageNotFound:
            print(f"Error: Docker image '{image}' not found.") # Basic logging
            # TODO: Implement image pulling or return error (Issue #XX)
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"Docker image '{image}' not found"}
        except docker.errors.APIError as e:
            print(f"Error allocating sandbox for app {appId}: {e}") # Basic logging
            # TODO: Log this error properly and return a proper error response (Issue #XX)
            return {"success": False, "message": f"Docker API error: {e}"}
        except Exception as e:
            print(f"An unexpected error occurred during sandbox allocation for app {appId}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"An unexpected error occurred: {e}"}


    async def release_sandbox(self, appId: str, sandbox_id: str): # TODO: Return a proper response (Issue #XX)
        """
        Releases a sandbox (Docker container).
        For POC, stops and removes the container. In a pooled system, it might return
        the container to the pool.

        Args:
            appId: The ID of the application the sandbox belongs to.
            sandbox_id: The ID of the sandbox container to release.
        """
        if not self._docker_client:
            print("Warning: Docker client not initialized. Cannot release sandbox.") # Basic logging
            return # TODO: Return a proper response (Issue #XX)

        try:
            container = self._docker_client.containers.get(sandbox_id)
            # Optional: Verify container belongs to the correct app_id
            if container.labels.get("app_id") != appId:
                 print(f"Warning: Container {sandbox_id} does not belong to app {appId}. Not releasing.") # Basic logging
                 return # TODO: Return a proper error/warning response (Issue #XX)

            print(f"Stopping and removing sandbox container {sandbox_id} for app {appId}.") # Basic logging
            container.stop()
            container.remove()
            print(f"Sandbox container {sandbox_id} released for app {appId}.") # Basic logging
            # TODO: Update internal state/pool (Issue #XX)
            # TODO: Return a proper success response (Issue #XX)
        except docker.errors.NotFound:
            print(f"Warning: Sandbox container {sandbox_id} not found for release.") # Basic logging
            # TODO: Return a proper error/warning response (Issue #XX)
        except docker.errors.APIError as e:
            print(f"Error releasing sandbox {sandbox_id} for app {appId}: {e}") # Basic logging
            # TODO: Log this error properly and return a proper error response (Issue #XX)
        except Exception as e:
            print(f"An unexpected error occurred during sandbox release for app {appId}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)


    async def start_application_sandboxes(self, appId: str): # TODO: Return a proper response (Issue #XX)
        """
        Starts all sandboxes associated with a specific application.

        Args:
            appId: The ID of the application.
        """
        if not self._docker_client:
            print("Warning: Docker client not initialized. Cannot start sandboxes.") # Basic logging
            return # TODO: Return a proper response (Issue #XX)

        sandboxes = await self._get_app_sandboxes(appId)
        if not sandboxes:
            print(f"No sandboxes found for app {appId} to start.") # Basic logging
            return # TODO: Return a proper response (Issue #XX)

        print(f"Starting {len(sandboxes)} sandbox(es) for app {appId}.") # Basic logging
        for container in sandboxes:
            try:
                container.start()
                print(f"Started sandbox container: {container.id}") # Basic logging
            except docker.errors.APIError as e:
                print(f"Error starting sandbox container {container.id} for app {appId}: {e}") # Basic logging
                # TODO: Log this error properly (Issue #XX)
            except Exception as e:
                print(f"An unexpected error occurred starting sandbox {container.id} for app {appId}: {e}") # Basic logging
                # TODO: Log this error properly (Issue #XX)

        # TODO: Return a proper success/status response (Issue #XX)


    async def stop_application_sandboxes(self, appId: str): # TODO: Return a proper response (Issue #XX)
        """
        Stops all sandboxes associated with a specific application.

        Args:
            appId: The ID of the application.
        """
        if not self._docker_client:
            print("Warning: Docker client not initialized. Cannot stop sandboxes.") # Basic logging
            return # TODO: Return a proper response (Issue #XX)

        sandboxes = await self._get_app_sandboxes(appId)
        if not sandboxes:
            print(f"No sandboxes found for app {appId} to stop.") # Basic logging
            return # TODO: Return a proper response (Issue #XX)

        print(f"Stopping {len(sandboxes)} sandbox(es) for app {appId}.") # Basic logging
        for container in sandboxes:
            try:
                container.stop()
                print(f"Stopped sandbox container: {container.id}") # Basic logging
            except docker.errors.APIError as e:
                print(f"Error stopping sandbox container {container.id} for app {appId}: {e}") # Basic logging
                # TODO: Log this error properly (Issue #XX)
            except Exception as e:
                print(f"An unexpected error occurred stopping sandbox {container.id} for app {appId}: {e}") # Basic logging
                # TODO: Log this error properly (Issue #XX)

        # TODO: Return a proper success/status response (Issue #XX)


    async def restart_application_sandboxes(self, appId: str): # TODO: Return a proper response (Issue #XX)
        """
        Restarts all sandboxes associated with a specific application.

        Args:
            appId: The ID of the application.
        """
        if not self._docker_client:
            print("Warning: Docker client not initialized. Cannot restart sandboxes.") # Basic logging
            return # TODO: Return a proper response (Issue #XX)

        sandboxes = await self._get_app_sandboxes(appId)
        if not sandboxes:
            print(f"No sandboxes found for app {appId} to restart.") # Basic logging
            return # TODO: Return a proper response (Issue #XX)

        print(f"Restarting {len(sandboxes)} sandbox(es) for app {appId}.") # Basic logging
        for container in sandboxes:
            try:
                container.restart()
                print(f"Restarted sandbox container: {container.id}") # Basic logging
            except docker.errors.APIError as e:
                print(f"Error restarting sandbox container {container.id} for app {appId}: {e}") # Basic logging
                # TODO: Log this error properly (Issue #XX)
            except Exception as e:
                print(f"An unexpected error occurred restarting sandbox {container.id} for app {appId}: {e}") # Basic logging
                # TODO: Log this error properly (Issue #XX)

        # TODO: Return a proper success/status response (Issue #XX)


    async def get_application_sandbox_status(self, appId: str) -> List[SandboxStatus]: # TODO: Return a proper response (Issue #XX)
        """
        Retrieves the status of all sandboxes associated with a specific application.

        Args:
            appId: The ID of the application.

        Returns:
            A list of SandboxStatus objects for the application's sandboxes.
        """
        if not self._docker_client:
            print("Warning: Docker client not initialized. Cannot get sandbox status.") # Basic logging
            return [] # TODO: Return a proper response (Issue #XX)

        sandboxes = await self._get_app_sandboxes(appId)
        status_list: List[SandboxStatus] = []
        print(f"Getting status for {len(sandboxes)} sandbox(es) for app {appId}.") # Basic logging
        for container in sandboxes:
            try:
                container.reload() # Get updated status
                status_list.append(SandboxStatus(
                    sandboxId=container.id,
                    appId=appId,
                    status=container.status, # Docker container status (running, exited, etc.)
                    image=container.image.tags[0] if container.image.tags else container.image.id, # Get image name/id
                    created=container.attrs.get("Created"),
                    started_at=container.attrs.get("State", {}).get("StartedAt"),
                    finished_at=container.attrs.get("State", {}).get("FinishedAt"),
                    exit_code=container.attrs.get("State", {}).get("ExitCode"),
                    # TODO: Add more details like resource usage, network info, etc. (Issue #XX)
                ))
            except docker.errors.NotFound:
                print(f"Warning: Sandbox container {container.id} not found during status check.") # Basic logging
                # Add a status indicating not found?
                status_list.append(SandboxStatus(sandboxId=container.id, appId=appId, status="not_found"))
            except docker.errors.APIError as e:
                print(f"Error getting status for sandbox container {container.id} for app {appId}: {e}") # Basic logging
                # TODO: Log this error properly (Issue #XX)
                status_list.append(SandboxStatus(sandboxId=container.id, appId=appId, status="error", details=str(e)))
            except Exception as e:
                print(f"An unexpected error occurred getting status for sandbox {container.id} for app {appId}: {e}") # Basic logging
                # TODO: Log this error properly (Issue #XX)
                status_list.append(SandboxStatus(sandboxId=container.id, appId=appId, status="error", details=str(e)))

        return status_list


    async def execute_command_in_sandbox(self, appId: str, sandbox_id: str, command: str) -> Dict[str, Any]: # TODO: Return command output/status (Issue #XX)
        """
        Executes a command inside a running sandbox container.
        For POC, uses container.exec_run.

        Args:
            appId: The ID of the application the sandbox belongs to.
            sandbox_id: The ID of the sandbox container.
            command: The command string to execute inside the container.

        Returns:
            A dictionary containing the command's exit code, stdout, and stderr.
        """
        if not self._docker_client:
            print("Error: Docker client not initialized. Cannot execute command.") # Basic logging
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": "Docker client not initialized"}

        try:
            container = self._docker_client.containers.get(sandbox_id)
            # Optional: Verify container belongs to the correct app_id
            if container.labels.get("app_id") != appId:
                 print(f"Warning: Container {sandbox_id} does not belong to app {appId}. Not executing command.") # Basic logging
                 # TODO: Return a proper error/warning response (Issue #XX)
                 return {"success": False, "message": f"Container {sandbox_id} does not belong to app {appId}"}

            print(f"Executing command '{command}' in sandbox {sandbox_id} for app {appId}.") # Basic logging
            # TODO: Implement security considerations for command execution (e.g., user, working_dir, environment) (Issue #XX)
            # TODO: Use hardened wrappers if available (as per security rules) (Issue #XX)
            exec_result = container.exec_run(command, stream=False, demux=True) # stream=False for simple output

            stdout = exec_result.output[0].decode('utf-8') if exec_result.output and exec_result.output[0] else ""
            stderr = exec_result.output[1].decode('utf-8') if exec_result.output and exec_result.output[1] else ""

            print(f"Command executed in sandbox {sandbox_id} complete. Exit Code: {exec_result.exit_code}") # Basic logging
            # print(f"Stdout:\n{stdout}") # Optional: Log stdout/stderr
            # print(f"Stderr:\n{stderr}")

            # TODO: Return a proper response including exit code, stdout, stderr (Issue #XX)
            return {"success": True, "exit_code": exec_result.exit_code, "stdout": stdout, "stderr": stderr}

        except docker.errors.NotFound:
            print(f"Error: Sandbox container {sandbox_id} not found for command execution.") # Basic logging
            # TODO: Return a proper error response (Issue #XX)
            return {"success": False, "message": f"Sandbox container {sandbox_id} not found"}
        except docker.errors.APIError as e:
            print(f"Error executing command in sandbox {sandbox_id} for app {appId}: {e}") # Basic logging
            # TODO: Log this error properly and return a proper error response (Issue #XX)
            return {"success": False, "message": f"Docker API error during command execution: {e}"}
        except Exception as e:
            print(f"An unexpected error occurred executing command in sandbox {sandbox_id} for app {appId}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            return {"success": False, "message": f"An unexpected error occurred: {e}"}


    # TODO: Add internal methods for interacting with the Docker API (Issue #XX)
    # TODO: Add internal methods for managing sandbox pools and scaling (Issue #XX)
    # TODO: Add internal methods for handling sandbox health checks (Issue #XX)
