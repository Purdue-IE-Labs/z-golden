from . import base_data_pb2 as _base_data_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TagUpdate(_message.Message):
    __slots__ = ("tags", "meta_ts")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _base_data_pb2.BaseData
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_base_data_pb2.BaseData, _Mapping]] = ...) -> None: ...
    TAGS_FIELD_NUMBER: _ClassVar[int]
    META_TS_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.MessageMap[int, _base_data_pb2.BaseData]
    meta_ts: int
    def __init__(self, tags: _Optional[_Mapping[int, _base_data_pb2.BaseData]] = ..., meta_ts: _Optional[int] = ...) -> None: ...

class MethodCall(_message.Message):
    __slots__ = ("params",)
    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _base_data_pb2.BaseData
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_base_data_pb2.BaseData, _Mapping]] = ...) -> None: ...
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _containers.MessageMap[int, _base_data_pb2.BaseData]
    def __init__(self, params: _Optional[_Mapping[int, _base_data_pb2.BaseData]] = ...) -> None: ...
