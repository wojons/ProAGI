from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import state_manager_pb2 as _state_manager_pb2
import application_registry_pb2 as _application_registry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogMessage(_message.Message):
    __slots__ = ("level", "message", "component_name", "traceId", "appId", "requestId", "taskId", "context", "timestamp", "metadata")
    class ContextEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _any_pb2.Any
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_NAME_FIELD_NUMBER: _ClassVar[int]
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    TASKID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    level: str
    message: str
    component_name: str
    traceId: str
    appId: str
    requestId: str
    taskId: str
    context: _containers.ScalarMap[str, str]
    timestamp: _timestamp_pb2.Timestamp
    metadata: _containers.MessageMap[str, _any_pb2.Any]
    def __init__(self, level: _Optional[str] = ..., message: _Optional[str] = ..., component_name: _Optional[str] = ..., traceId: _Optional[str] = ..., appId: _Optional[str] = ..., requestId: _Optional[str] = ..., taskId: _Optional[str] = ..., context: _Optional[_Mapping[str, str]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., metadata: _Optional[_Mapping[str, _any_pb2.Any]] = ...) -> None: ...

class Metric(_message.Message):
    __slots__ = ("name", "type", "value", "labels", "appId", "traceId", "requestId")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    value: float
    labels: _containers.ScalarMap[str, str]
    appId: str
    traceId: str
    requestId: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., value: _Optional[float] = ..., labels: _Optional[_Mapping[str, str]] = ..., appId: _Optional[str] = ..., traceId: _Optional[str] = ..., requestId: _Optional[str] = ...) -> None: ...

class LogFrameworkMessageRequest(_message.Message):
    __slots__ = ("log_message",)
    LOG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    log_message: LogMessage
    def __init__(self, log_message: _Optional[_Union[LogMessage, _Mapping]] = ...) -> None: ...

class LogFrameworkMessageResponse(_message.Message):
    __slots__ = ("success", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class RecordMetricRequest(_message.Message):
    __slots__ = ("metric",)
    METRIC_FIELD_NUMBER: _ClassVar[int]
    metric: Metric
    def __init__(self, metric: _Optional[_Union[Metric, _Mapping]] = ...) -> None: ...

class RecordMetricResponse(_message.Message):
    __slots__ = ("success", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class GetConfigValueRequest(_message.Message):
    __slots__ = ("appId", "key", "componentId")
    APPID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    COMPONENTID_FIELD_NUMBER: _ClassVar[int]
    appId: str
    key: str
    componentId: str
    def __init__(self, appId: _Optional[str] = ..., key: _Optional[str] = ..., componentId: _Optional[str] = ...) -> None: ...

class GetConfigValueResponse(_message.Message):
    __slots__ = ("success", "key", "value", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    key: str
    value: _any_pb2.Any
    error_message: str
    def __init__(self, success: bool = ..., key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...
