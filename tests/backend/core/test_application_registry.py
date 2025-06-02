import pytest
from unittest.mock import AsyncMock, MagicMock # For mocking async and sync methods

from backend.src.core.application_registry.application_registry import ApplicationRegistry
from core.shared.data_models.data_models import AppDefinition, AppStatus
from core.interfaces.state_manager_interface import StateManagerInterface
from sqlmodel import Session


@pytest.fixture
def mock_state_manager():
    """Fixture to create a mock StateManagerInterface."""
    mock = AsyncMock(spec=StateManagerInterface)
    # Setup default return values for common methods if needed
    mock.get_definition_file_content.return_value = None # Default to not found
    mock.set_definition_file_content.return_value = None # Default success (no specific return)
    mock.delete_definition_file.return_value = None # Default success
    return mock

@pytest.fixture
def mock_db_session():
    """Fixture to create a mock database session."""
    return MagicMock(spec=Session)

@pytest.fixture
def app_registry(mock_state_manager, mock_db_session):
    """Fixture to create an ApplicationRegistry instance with mock dependencies."""
    return ApplicationRegistry(state_manager=mock_state_manager, db_session=mock_db_session)

@pytest.fixture
def sample_app_definition():
    """Fixture to provide a sample AppDefinition."""
    return AppDefinition(
        appId="test_app_001",
        name="Test Application",
        description="A sample application for testing.",
        version="1.0.0",
        entryPoint="sandbox://docker/test-image",
        # Add other required fields with default/sample values
        roles=[],
        exposedTools=[],
        exposedResources=[],
        dependencies=[],
        sandboxPools=[],
        components={},
        config={},
        permissions=[]
    )

@pytest.mark.asyncio
async def test_register_application_success(app_registry, mock_state_manager, sample_app_definition):
    """Test successful application registration."""
    # Arrange
    mock_state_manager.get_definition_file_content.return_value = None # Ensure app doesn't exist

    # Act
    result = await app_registry.register_application(sample_app_definition)

    # Assert
    assert result["success"] is True
    assert result["appId"] == sample_app_definition.appId
    assert result["status"] == AppStatus.INITIALIZING
    mock_state_manager.set_definition_file_content.assert_called_once()
    # TODO: Add more specific assertions about the content saved (Issue #XX)

@pytest.mark.asyncio
async def test_register_application_already_exists(app_registry, mock_state_manager, sample_app_definition):
    """Test registration when application already exists."""
    # Arrange
    # Simulate app already exists by having _get_app_definition return it
    app_registry._get_app_definition = AsyncMock(return_value=sample_app_definition)

    # Act
    result = await app_registry.register_application(sample_app_definition)

    # Assert
    assert result["success"] is False
    assert "already exists" in result["message"]
    mock_state_manager.set_definition_file_content.assert_not_called()

@pytest.mark.asyncio
async def test_get_application_details_success(app_registry, sample_app_definition):
    """Test retrieving details for an existing application."""
    # Arrange
    app_registry._get_app_definition = AsyncMock(return_value=sample_app_definition)

    # Act
    result = await app_registry.get_application_details(sample_app_definition.appId)

    # Assert
    assert result["success"] is True
    assert result["definition"] == sample_app_definition

@pytest.mark.asyncio
async def test_get_application_details_not_found(app_registry):
    """Test retrieving details for a non-existent application."""
    # Arrange
    app_registry._get_app_definition = AsyncMock(return_value=None)

    # Act
    result = await app_registry.get_application_details("non_existent_app")

    # Assert
    assert result["success"] is False
    assert "not found" in result["message"]

@pytest.mark.asyncio
async def test_update_application_success(app_registry, mock_state_manager, sample_app_definition):
    """Test successful application update."""
    # Arrange
    app_registry._get_app_definition = AsyncMock(return_value=sample_app_definition)
    updated_fields = {"version": "1.0.1", "description": "Updated description"}

    # Act
    result = await app_registry.update_application(sample_app_definition.appId, None, updated_fields)

    # Assert
    assert result["success"] is True
    assert result["appId"] == sample_app_definition.appId
    mock_state_manager.set_definition_file_content.assert_called_once()
    # TODO: Verify that the definition passed to set_definition_file_content has the updated fields (Issue #XX)

@pytest.mark.asyncio
async def test_update_application_not_found(app_registry, mock_state_manager):
    """Test updating a non-existent application."""
    # Arrange
    app_registry._get_app_definition = AsyncMock(return_value=None)
    updated_fields = {"version": "1.0.1"}

    # Act
    result = await app_registry.update_application("non_existent_app", None, updated_fields)

    # Assert
    assert result["success"] is False
    assert "not found" in result["message"]
    mock_state_manager.set_definition_file_content.assert_not_called()

@pytest.mark.asyncio
async def test_deregister_application_success(app_registry, mock_state_manager, sample_app_definition):
    """Test successful application deregistration."""
    # Arrange
    app_registry._get_app_definition = AsyncMock(return_value=sample_app_definition)
    app_registry._active_applications[sample_app_definition.appId] = AppStatus.ACTIVE

    # Act
    result = await app_registry.deregister_application(sample_app_definition.appId, deleteState=True)

    # Assert
    assert result["success"] is True
    assert result["appId"] == sample_app_definition.appId
    mock_state_manager.delete_definition_file.assert_called_once_with(
        sample_app_definition.appId,
        "app_definition.yaml",
        f"Deregister application {sample_app_definition.appId} and delete state"
    )
    assert sample_app_definition.appId not in app_registry._active_applications

@pytest.mark.asyncio
async def test_deregister_application_not_found(app_registry, mock_state_manager):
    """Test deregistering a non-existent application."""
    # Arrange
    app_registry._get_app_definition = AsyncMock(return_value=None)

    # Act
    result = await app_registry.deregister_application("non_existent_app")

    # Assert
    assert result["success"] is False
    assert "not found" in result["message"]
    mock_state_manager.delete_definition_file.assert_not_called()

@pytest.mark.asyncio
async def test_list_active_applications(app_registry, sample_app_definition):
    """Test listing active applications."""
    # Arrange
    app_id = sample_app_definition.appId
    app_registry._active_applications = {app_id: AppStatus.ACTIVE}

    # Act
    result = await app_registry.list_active_applications()

    # Assert
    assert "applications" in result
    assert len(result["applications"]) == 1
    assert result["applications"][0]["appId"] == app_id
    assert result["applications"][0]["status"] == AppStatus.ACTIVE

# TODO: Add tests for get_sandbox_requirements (Issue #XX)
# TODO: Add tests for get_component_definition (Issue #XX)
# TODO: Add tests for get_app_configuration_value (Issue #XX)
# TODO: Add tests for validate_api_key (Issue #XX) - requires mocking db_session more extensively
# TODO: Add tests for get_application_permissions (Issue #XX)
# TODO: Add tests for get_user_permissions_for_app (Issue #XX)
