from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDefinitionFileContentRequest(_message.Message):
    __slots__ = ("app_id", "path")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    path: str
    def __init__(self, app_id: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class GetDefinitionFileContentResponse(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...

class SetDefinitionFileContentRequest(_message.Message):
    __slots__ = ("app_id", "path", "content", "commit_message")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    path: str
    content: str
    commit_message: str
    def __init__(self, app_id: _Optional[str] = ..., path: _Optional[str] = ..., content: _Optional[str] = ..., commit_message: _Optional[str] = ...) -> None: ...

class SetDefinitionFileContentResponse(_message.Message):
    __slots__ = ("success", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class DeleteDefinitionFileRequest(_message.Message):
    __slots__ = ("app_id", "path", "commit_message")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    path: str
    commit_message: str
    def __init__(self, app_id: _Optional[str] = ..., path: _Optional[str] = ..., commit_message: _Optional[str] = ...) -> None: ...

class DeleteDefinitionFileResponse(_message.Message):
    __slots__ = ("success", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class ListDefinitionDirectoryRequest(_message.Message):
    __slots__ = ("app_id", "path", "recursive")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    RECURSIVE_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    path: str
    recursive: bool
    def __init__(self, app_id: _Optional[str] = ..., path: _Optional[str] = ..., recursive: bool = ...) -> None: ...

class FileInfo(_message.Message):
    __slots__ = ("name", "path", "type")
    class FileType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FILE: _ClassVar[FileInfo.FileType]
        DIRECTORY: _ClassVar[FileInfo.FileType]
    FILE: FileInfo.FileType
    DIRECTORY: FileInfo.FileType
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    path: str
    type: FileInfo.FileType
    def __init__(self, name: _Optional[str] = ..., path: _Optional[str] = ..., type: _Optional[_Union[FileInfo.FileType, str]] = ...) -> None: ...

class ListDefinitionDirectoryResponse(_message.Message):
    __slots__ = ("files", "success", "error_message")
    FILES_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[FileInfo]
    success: bool
    error_message: str
    def __init__(self, files: _Optional[_Iterable[_Union[FileInfo, _Mapping]]] = ..., success: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class GetRuntimeValueRequest(_message.Message):
    __slots__ = ("app_id", "key")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    key: str
    def __init__(self, app_id: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class GetRuntimeValueResponse(_message.Message):
    __slots__ = ("found", "value", "error_message")
    FOUND_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    found: bool
    value: str
    error_message: str
    def __init__(self, found: bool = ..., value: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class SetRuntimeValueRequest(_message.Message):
    __slots__ = ("app_id", "key", "value")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    key: str
    value: str
    def __init__(self, app_id: _Optional[str] = ..., key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class SetRuntimeValueResponse(_message.Message):
    __slots__ = ("success", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class DeleteRuntimeValueRequest(_message.Message):
    __slots__ = ("app_id", "key")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    key: str
    def __init__(self, app_id: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class DeleteRuntimeValueResponse(_message.Message):
    __slots__ = ("success", "error_message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ...) -> None: ...
