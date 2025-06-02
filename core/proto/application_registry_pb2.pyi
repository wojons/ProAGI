from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AppDefinition(_message.Message):
    __slots__ = ("appId", "name", "description", "sandboxPoolConfig", "componentRegistry", "config")
    class ComponentRegistryEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ComponentDefinition
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ComponentDefinition, _Mapping]] = ...) -> None: ...
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    APPID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SANDBOXPOOLCONFIG_FIELD_NUMBER: _ClassVar[int]
    COMPONENTREGISTRY_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    appId: str
    name: str
    description: str
    sandboxPoolConfig: SandboxPoolConfig
    componentRegistry: _containers.MessageMap[str, ComponentDefinition]
    config: _containers.ScalarMap[str, str]
    def __init__(self, appId: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., sandboxPoolConfig: _Optional[_Union[SandboxPoolConfig, _Mapping]] = ..., componentRegistry: _Optional[_Mapping[str, ComponentDefinition]] = ..., config: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SandboxPoolConfig(_message.Message):
    __slots__ = ("image", "min_instances", "max_instances")
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    MIN_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    MAX_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    image: str
    min_instances: int
    max_instances: int
    def __init__(self, image: _Optional[str] = ..., min_instances: _Optional[int] = ..., max_instances: _Optional[int] = ...) -> None: ...

class ComponentDefinition(_message.Message):
    __slots__ = ("componentId", "description", "execution_type")
    COMPONENTID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    componentId: str
    description: str
    execution_type: str
    def __init__(self, componentId: _Optional[str] = ..., description: _Optional[str] = ..., execution_type: _Optional[str] = ...) -> None: ...

class ToolDefinition(_message.Message):
    __slots__ = ("name", "description", "input_schema_json", "output_schema_json", "source")
    class SourceEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INPUT_SCHEMA_JSON_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_JSON_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    input_schema_json: str
    output_schema_json: str
    source: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., input_schema_json: _Optional[str] = ..., output_schema_json: _Optional[str] = ..., source: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ResourceDefinition(_message.Message):
    __slots__ = ("uri", "description", "schema_json", "source")
    class SourceEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    URI_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_JSON_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    uri: str
    description: str
    schema_json: str
    source: _containers.ScalarMap[str, str]
    def __init__(self, uri: _Optional[str] = ..., description: _Optional[str] = ..., schema_json: _Optional[str] = ..., source: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ServerStatus(_message.Message):
    __slots__ = ("name", "status")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: str
    def __init__(self, name: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class SandboxStatus(_message.Message):
    __slots__ = ("sandboxId", "appId", "status", "image", "created", "started_at", "finished_at", "exit_code", "details")
    class DetailsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SANDBOXID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    sandboxId: str
    appId: str
    status: str
    image: str
    created: str
    started_at: str
    finished_at: str
    exit_code: int
    details: _containers.ScalarMap[str, str]
    def __init__(self, sandboxId: _Optional[str] = ..., appId: _Optional[str] = ..., status: _Optional[str] = ..., image: _Optional[str] = ..., created: _Optional[str] = ..., started_at: _Optional[str] = ..., finished_at: _Optional[str] = ..., exit_code: _Optional[int] = ..., details: _Optional[_Mapping[str, str]] = ...) -> None: ...

class InterAppPermission(_message.Message):
    __slots__ = ("target_app_id", "permissions")
    TARGET_APP_ID_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    target_app_id: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, target_app_id: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ...) -> None: ...

class UserPermissionsForApp(_message.Message):
    __slots__ = ("userId", "appId", "permissions")
    USERID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    userId: str
    appId: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, userId: _Optional[str] = ..., appId: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ...) -> None: ...

class RegisterApplicationRequest(_message.Message):
    __slots__ = ("definition",)
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    definition: AppDefinition
    def __init__(self, definition: _Optional[_Union[AppDefinition, _Mapping]] = ...) -> None: ...

class RegisterApplicationResponse(_message.Message):
    __slots__ = ("success", "appId", "status", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    appId: str
    status: str
    error_message: str
    def __init__(self, success: bool = ..., appId: _Optional[str] = ..., status: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class UpdateApplicationRequest(_message.Message):
    __slots__ = ("appId", "update_mask", "updated_definition_fields")
    APPID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DEFINITION_FIELDS_FIELD_NUMBER: _ClassVar[int]
    appId: str
    update_mask: _containers.RepeatedScalarFieldContainer[str]
    updated_definition_fields: AppDefinition
    def __init__(self, appId: _Optional[str] = ..., update_mask: _Optional[_Iterable[str]] = ..., updated_definition_fields: _Optional[_Union[AppDefinition, _Mapping]] = ...) -> None: ...

class UpdateApplicationResponse(_message.Message):
    __slots__ = ("success", "appId", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    appId: str
    error_message: str
    def __init__(self, success: bool = ..., appId: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class DeregisterApplicationRequest(_message.Message):
    __slots__ = ("appId", "delete_state")
    APPID_FIELD_NUMBER: _ClassVar[int]
    DELETE_STATE_FIELD_NUMBER: _ClassVar[int]
    appId: str
    delete_state: bool
    def __init__(self, appId: _Optional[str] = ..., delete_state: bool = ...) -> None: ...

class DeregisterApplicationResponse(_message.Message):
    __slots__ = ("success", "appId", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    appId: str
    error_message: str
    def __init__(self, success: bool = ..., appId: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class GetApplicationStatusRequest(_message.Message):
    __slots__ = ("appId",)
    APPID_FIELD_NUMBER: _ClassVar[int]
    appId: str
    def __init__(self, appId: _Optional[str] = ...) -> None: ...

class GetApplicationStatusResponse(_message.Message):
    __slots__ = ("appId", "status")
    APPID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    appId: str
    status: str
    def __init__(self, appId: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class ListActiveApplicationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListActiveApplicationsResponse(_message.Message):
    __slots__ = ("applications",)
    APPLICATIONS_FIELD_NUMBER: _ClassVar[int]
    applications: _containers.RepeatedCompositeFieldContainer[GetApplicationStatusResponse]
    def __init__(self, applications: _Optional[_Iterable[_Union[GetApplicationStatusResponse, _Mapping]]] = ...) -> None: ...

class GetApplicationDetailsRequest(_message.Message):
    __slots__ = ("appId",)
    APPID_FIELD_NUMBER: _ClassVar[int]
    appId: str
    def __init__(self, appId: _Optional[str] = ...) -> None: ...

class GetApplicationDetailsResponse(_message.Message):
    __slots__ = ("success", "definition", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    definition: AppDefinition
    error_message: str
    def __init__(self, success: bool = ..., definition: _Optional[_Union[AppDefinition, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...

class GetSandboxRequirementsRequest(_message.Message):
    __slots__ = ("appId",)
    APPID_FIELD_NUMBER: _ClassVar[int]
    appId: str
    def __init__(self, appId: _Optional[str] = ...) -> None: ...

class GetSandboxRequirementsResponse(_message.Message):
    __slots__ = ("success", "sandbox_requirements", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SANDBOX_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    sandbox_requirements: SandboxPoolConfig
    error_message: str
    def __init__(self, success: bool = ..., sandbox_requirements: _Optional[_Union[SandboxPoolConfig, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...

class GetComponentDefinitionRequest(_message.Message):
    __slots__ = ("appId", "componentId", "route_input")
    class RouteInputEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    APPID_FIELD_NUMBER: _ClassVar[int]
    COMPONENTID_FIELD_NUMBER: _ClassVar[int]
    ROUTE_INPUT_FIELD_NUMBER: _ClassVar[int]
    appId: str
    componentId: str
    route_input: _containers.ScalarMap[str, str]
    def __init__(self, appId: _Optional[str] = ..., componentId: _Optional[str] = ..., route_input: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GetComponentDefinitionResponse(_message.Message):
    __slots__ = ("success", "component_definition", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    component_definition: ComponentDefinition
    error_message: str
    def __init__(self, success: bool = ..., component_definition: _Optional[_Union[ComponentDefinition, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...

class GetAppConfigurationValueRequest(_message.Message):
    __slots__ = ("appId", "key", "componentId")
    APPID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    COMPONENTID_FIELD_NUMBER: _ClassVar[int]
    appId: str
    key: str
    componentId: str
    def __init__(self, appId: _Optional[str] = ..., key: _Optional[str] = ..., componentId: _Optional[str] = ...) -> None: ...

class GetAppConfigurationValueResponse(_message.Message):
    __slots__ = ("success", "key", "value_json", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_JSON_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    key: str
    value_json: str
    error_message: str
    def __init__(self, success: bool = ..., key: _Optional[str] = ..., value_json: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class ValidateApiKeyRequest(_message.Message):
    __slots__ = ("api_key",)
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    def __init__(self, api_key: _Optional[str] = ...) -> None: ...

class ValidateApiKeyResponse(_message.Message):
    __slots__ = ("success", "appId", "userId", "permissions", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    appId: str
    userId: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    error_message: str
    def __init__(self, success: bool = ..., appId: _Optional[str] = ..., userId: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class GetApplicationPermissionsRequest(_message.Message):
    __slots__ = ("appId",)
    APPID_FIELD_NUMBER: _ClassVar[int]
    appId: str
    def __init__(self, appId: _Optional[str] = ...) -> None: ...

class GetApplicationPermissionsResponse(_message.Message):
    __slots__ = ("success", "permissions", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    permissions: _containers.RepeatedCompositeFieldContainer[InterAppPermission]
    error_message: str
    def __init__(self, success: bool = ..., permissions: _Optional[_Iterable[_Union[InterAppPermission, _Mapping]]] = ..., error_message: _Optional[str] = ...) -> None: ...

class GetUserPermissionsForAppRequest(_message.Message):
    __slots__ = ("appId", "userId")
    APPID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    appId: str
    userId: str
    def __init__(self, appId: _Optional[str] = ..., userId: _Optional[str] = ...) -> None: ...

class GetUserPermissionsForAppResponse(_message.Message):
    __slots__ = ("success", "userId", "appId", "permissions", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    userId: str
    appId: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    error_message: str
    def __init__(self, success: bool = ..., userId: _Optional[str] = ..., appId: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ..., error_message: _Optional[str] = ...) -> None: ...
