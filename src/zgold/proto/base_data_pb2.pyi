from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListInt(_message.Message):
    __slots__ = ("list",)
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, list: _Optional[_Iterable[int]] = ...) -> None: ...

class ListLong(_message.Message):
    __slots__ = ("list",)
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, list: _Optional[_Iterable[int]] = ...) -> None: ...

class ListFloat(_message.Message):
    __slots__ = ("list",)
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, list: _Optional[_Iterable[float]] = ...) -> None: ...

class ListString(_message.Message):
    __slots__ = ("list",)
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, list: _Optional[_Iterable[str]] = ...) -> None: ...

class ListBool(_message.Message):
    __slots__ = ("list",)
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, list: _Optional[_Iterable[bool]] = ...) -> None: ...

class ListDatetime(_message.Message):
    __slots__ = ("list",)
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    def __init__(self, list: _Optional[_Iterable[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]]] = ...) -> None: ...

class BaseData(_message.Message):
    __slots__ = ("int_data", "long_data", "float_data", "string_data", "bool_data", "datetime_data", "list_int_data", "list_long_data", "list_float_data", "list_string_data", "list_bool_data", "list_datetime_data")
    INT_DATA_FIELD_NUMBER: _ClassVar[int]
    LONG_DATA_FIELD_NUMBER: _ClassVar[int]
    FLOAT_DATA_FIELD_NUMBER: _ClassVar[int]
    STRING_DATA_FIELD_NUMBER: _ClassVar[int]
    BOOL_DATA_FIELD_NUMBER: _ClassVar[int]
    DATETIME_DATA_FIELD_NUMBER: _ClassVar[int]
    LIST_INT_DATA_FIELD_NUMBER: _ClassVar[int]
    LIST_LONG_DATA_FIELD_NUMBER: _ClassVar[int]
    LIST_FLOAT_DATA_FIELD_NUMBER: _ClassVar[int]
    LIST_STRING_DATA_FIELD_NUMBER: _ClassVar[int]
    LIST_BOOL_DATA_FIELD_NUMBER: _ClassVar[int]
    LIST_DATETIME_DATA_FIELD_NUMBER: _ClassVar[int]
    int_data: int
    long_data: int
    float_data: float
    string_data: str
    bool_data: bool
    datetime_data: _timestamp_pb2.Timestamp
    list_int_data: ListInt
    list_long_data: ListLong
    list_float_data: ListFloat
    list_string_data: ListString
    list_bool_data: ListBool
    list_datetime_data: ListDatetime
    def __init__(self, int_data: _Optional[int] = ..., long_data: _Optional[int] = ..., float_data: _Optional[float] = ..., string_data: _Optional[str] = ..., bool_data: bool = ..., datetime_data: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., list_int_data: _Optional[_Union[ListInt, _Mapping]] = ..., list_long_data: _Optional[_Union[ListLong, _Mapping]] = ..., list_float_data: _Optional[_Union[ListFloat, _Mapping]] = ..., list_string_data: _Optional[_Union[ListString, _Mapping]] = ..., list_bool_data: _Optional[_Union[ListBool, _Mapping]] = ..., list_datetime_data: _Optional[_Union[ListDatetime, _Mapping]] = ...) -> None: ...
