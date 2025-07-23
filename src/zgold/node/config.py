import json5
from typing import Any, Dict, Self

from zgold.proto import config_pb2

# Proto classes
Meta = config_pb2.Meta
DataItemConfig = config_pb2.DataItemConfig
DataModelRef = config_pb2.DataModelRef
Prop = config_pb2.Prop
DataModelConfig = config_pb2.DataModelConfig
MethodConfig = config_pb2.MethodConfig
ResponseConfig = config_pb2.ResponseConfig
SubnodeConfig = config_pb2.SubnodeConfig
BaseType = config_pb2.BaseType

# TODO: Validate names against reserved keywords and characters in various programming languages and OS
class NodeConfig:
    """
    Load a JSON5-based configuration and compile it into a protobuf Meta message.
    """

    def __init__(self, meta: Meta):
        self.meta = meta
        # method callbacks
        # model file locations

    @classmethod
    def from_json5(cls, path: str) -> Self:
        # Parse the JSON5 file
        with open(path, 'r') as fp:
            raw = json5.load(fp)
        m = Meta()
        m.node_key = raw['key']

        # Tags
        for tag in raw.get('tags', []):
            m.tags.append(cls._build_data_item_config(tag))

        # Models
        # TODO: Read from set model dir
        # for model in raw.get('models', []):
        #     m.models.append(cls._build_data_model_config(model))

        # Methods
        for method in raw.get('methods', []):
            m.methods.append(cls._build_method_config(method))

        # Subnodes
        for sub in raw.get('subnodes', []):
            m.subnodes.append(cls._build_subnode_config(sub))

        # Props
        for key, val in raw.get('props', {}).items():
            m.props.append(cls._build_prop(key, val))

        return cls(m)
    
    def use_models_at(path: str):
        pass

    @classmethod
    def _build_data_item_config(cls, cfg: Dict[str, Any]) -> DataItemConfig:
        # path, alias, is_list, oneof{model, base}, props
        # TODO: Add unique int alias to every data item 
        item = DataItemConfig()
        item.path = cfg['path']
        item.is_list = isinstance(cfg.get('type'), str) and cfg['type'].startswith('list[')
        type_str = cfg['type']

        # Unwrap list[...] if present
        inner = type_str[5:-1] if item.is_list else type_str

        if inner == 'model':
            item.model.model_path = cfg['model_path']
            item.model.model_version = cfg.get('model_version', cls._default_model_version(cfg['model_path']))
        else:
            item.base = cls._map_base_type(inner)

        # Attach any props
        for k, v in cfg.get('props', {}).items():
            item.props.append(cls._build_prop(k, v))

        return item

    @classmethod
    def _build_data_model_config(cls, cfg: Dict[str, Any]) -> DataModelConfig:
        dm = DataModelConfig()
        dm.path = cfg['path']
        dm.version = cfg['version']
        for itm in cfg.get('items', []):
            dm.items.append(cls._build_data_item_config(itm))
        return dm

    @classmethod
    def _build_method_config(cls, cfg: Dict[str, Any]) -> MethodConfig:
        mc = MethodConfig()
        mc.path = cfg['path']
        for p in cfg.get('params', []):
            mc.params.append(cls._build_data_item_config(p))
        for r in cfg.get('responses', []):
            mc.responses.append(cls._build_response_config(r))
        return mc

    @classmethod
    def _build_response_config(cls, cfg: Dict[str, Any]) -> ResponseConfig:
        rc = ResponseConfig()
        rc.code = cfg['code']
        rc.type = config_pb2.ResponseType.Value(cfg['type'])
        for p in cfg.get('props', []):
            rc.props.append(cls._build_prop(p['key'], p['value']))
        for b in cfg.get('body', []):
            rc.body.append(cls._build_data_item_config(b))
        return rc

    @classmethod
    def _build_subnode_config(cls, cfg: Dict[str, Any]) -> SubnodeConfig:
        sn = SubnodeConfig()
        sn.path = cfg['path']
        for t in cfg.get('tags', []):
            sn.tags.append(cls._build_data_item_config(t))
        for m in cfg.get('methods', []):
            sn.methods.append(cls._build_method_config(m))
        for s in cfg.get('subnodes', []):
            sn.subnodes.append(cls._build_subnode_config(s))
        for key, val in cfg.get('props', {}).items():
            sn.props.append(cls._build_prop(key, val))
        return sn

    @classmethod
    def _build_prop(cls, key: str, val: Any) -> Prop:
        p = Prop()
        p.key = key
        # TODO: Support all basedata types (except int, that will always map to long most likely)
        p.type = BaseType.STRING
        p.value.string_data = str(val)
        return p

    @staticmethod
    def _map_base_type(name: str) -> BaseType:
        mapping = {
            'int': BaseType.INT,
            'long': BaseType.LONG,
            'float': BaseType.FLOAT,
            'string': BaseType.STRING,
            'bool': BaseType.BOOL,
            'datetime': BaseType.DATETIME,
        }
        try:
            return mapping[name]
        except KeyError:
            raise ValueError(f"Unknown base type: {name}")

    @staticmethod
    def _default_model_version(model_path: str) -> int:
        # TODO: scan model directory to pick latest version
        return 1
