from . import base_data_pb2 as _base_data_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BaseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[BaseType]
    INT: _ClassVar[BaseType]
    LONG: _ClassVar[BaseType]
    FLOAT: _ClassVar[BaseType]
    STRING: _ClassVar[BaseType]
    BOOL: _ClassVar[BaseType]
    DATETIME: _ClassVar[BaseType]

class ResponseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OK: _ClassVar[ResponseType]
    ERR: _ClassVar[ResponseType]
    INFO: _ClassVar[ResponseType]
UNKNOWN: BaseType
INT: BaseType
LONG: BaseType
FLOAT: BaseType
STRING: BaseType
BOOL: BaseType
DATETIME: BaseType
OK: ResponseType
ERR: ResponseType
INFO: ResponseType

class DataItemConfig(_message.Message):
    __slots__ = ("path", "alias", "is_list", "model", "base", "props")
    PATH_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    IS_LIST_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    BASE_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    path: str
    alias: int
    is_list: bool
    model: DataModelRef
    base: BaseType
    props: _containers.RepeatedCompositeFieldContainer[Prop]
    def __init__(self, path: _Optional[str] = ..., alias: _Optional[int] = ..., is_list: bool = ..., model: _Optional[_Union[DataModelRef, _Mapping]] = ..., base: _Optional[_Union[BaseType, str]] = ..., props: _Optional[_Iterable[_Union[Prop, _Mapping]]] = ...) -> None: ...

class DataModelRef(_message.Message):
    __slots__ = ("model_path", "model_version")
    MODEL_PATH_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    model_path: str
    model_version: int
    def __init__(self, model_path: _Optional[str] = ..., model_version: _Optional[int] = ...) -> None: ...

class Prop(_message.Message):
    __slots__ = ("key", "type", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    type: BaseType
    value: _base_data_pb2.BaseData
    def __init__(self, key: _Optional[str] = ..., type: _Optional[_Union[BaseType, str]] = ..., value: _Optional[_Union[_base_data_pb2.BaseData, _Mapping]] = ...) -> None: ...

class DataModelConfig(_message.Message):
    __slots__ = ("path", "version", "items")
    PATH_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    path: str
    version: int
    items: _containers.RepeatedCompositeFieldContainer[DataItemConfig]
    def __init__(self, path: _Optional[str] = ..., version: _Optional[int] = ..., items: _Optional[_Iterable[_Union[DataItemConfig, _Mapping]]] = ...) -> None: ...

class MethodConfig(_message.Message):
    __slots__ = ("path", "params", "responses")
    PATH_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    path: str
    params: _containers.RepeatedCompositeFieldContainer[DataItemConfig]
    responses: _containers.RepeatedCompositeFieldContainer[ResponseConfig]
    def __init__(self, path: _Optional[str] = ..., params: _Optional[_Iterable[_Union[DataItemConfig, _Mapping]]] = ..., responses: _Optional[_Iterable[_Union[ResponseConfig, _Mapping]]] = ...) -> None: ...

class ResponseConfig(_message.Message):
    __slots__ = ("code", "type", "props", "body")
    CODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    code: int
    type: ResponseType
    props: _containers.RepeatedCompositeFieldContainer[Prop]
    body: _containers.RepeatedCompositeFieldContainer[DataItemConfig]
    def __init__(self, code: _Optional[int] = ..., type: _Optional[_Union[ResponseType, str]] = ..., props: _Optional[_Iterable[_Union[Prop, _Mapping]]] = ..., body: _Optional[_Iterable[_Union[DataItemConfig, _Mapping]]] = ...) -> None: ...

class SubnodeConfig(_message.Message):
    __slots__ = ("path", "tags", "methods", "subnodes", "props")
    PATH_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    METHODS_FIELD_NUMBER: _ClassVar[int]
    SUBNODES_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    path: str
    tags: _containers.RepeatedCompositeFieldContainer[DataItemConfig]
    methods: _containers.RepeatedCompositeFieldContainer[MethodConfig]
    subnodes: _containers.RepeatedCompositeFieldContainer[SubnodeConfig]
    props: _containers.RepeatedCompositeFieldContainer[Prop]
    def __init__(self, path: _Optional[str] = ..., tags: _Optional[_Iterable[_Union[DataItemConfig, _Mapping]]] = ..., methods: _Optional[_Iterable[_Union[MethodConfig, _Mapping]]] = ..., subnodes: _Optional[_Iterable[_Union[SubnodeConfig, _Mapping]]] = ..., props: _Optional[_Iterable[_Union[Prop, _Mapping]]] = ...) -> None: ...

class Meta(_message.Message):
    __slots__ = ("node_key", "tags", "methods", "subnodes", "models", "props")
    NODE_KEY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    METHODS_FIELD_NUMBER: _ClassVar[int]
    SUBNODES_FIELD_NUMBER: _ClassVar[int]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    node_key: str
    tags: _containers.RepeatedCompositeFieldContainer[DataItemConfig]
    methods: _containers.RepeatedCompositeFieldContainer[MethodConfig]
    subnodes: _containers.RepeatedCompositeFieldContainer[SubnodeConfig]
    models: _containers.RepeatedCompositeFieldContainer[DataModelConfig]
    props: _containers.RepeatedCompositeFieldContainer[Prop]
    def __init__(self, node_key: _Optional[str] = ..., tags: _Optional[_Iterable[_Union[DataItemConfig, _Mapping]]] = ..., methods: _Optional[_Iterable[_Union[MethodConfig, _Mapping]]] = ..., subnodes: _Optional[_Iterable[_Union[SubnodeConfig, _Mapping]]] = ..., models: _Optional[_Iterable[_Union[DataModelConfig, _Mapping]]] = ..., props: _Optional[_Iterable[_Union[Prop, _Mapping]]] = ...) -> None: ...
