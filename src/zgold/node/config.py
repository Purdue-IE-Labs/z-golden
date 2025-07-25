import json5
from typing import Any, Dict, Self
import pathlib

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
        self.models_used : set[str] = set()

    @classmethod
    # default to ./models
    def from_json5(cls, path: str, models_dir: str) -> Self:
        # Parse the JSON5 file
        with open(path, 'r') as fp:
            raw = json5.load(fp)
        m = Meta()
        cfg = cls(m)
        cfg.meta.node_key = raw['key']

        # Tags
        for tag in raw.get('tags', []):
            cfg.meta.tags.append(cfg._build_data_item_config(tag))

        # Methods
        for method in raw.get('methods', []):
            cfg.meta.methods.append(cfg._build_method_config(method))
 
        # Subnodes
        for sub in raw.get('subnodes', []):
            cfg.meta.subnodes.append(cfg._build_subnode_config(sub))

        # Props
        for k, v in raw.get('props', {}).items():
            cfg.meta.props.append(cfg._build_prop(k, v))

        # Models
        if len(cfg.models_used) > 0 :
            if not pathlib.Path(models_dir).exists():
                raise ValueError(f"Model configuration at path {path} does not exist")
            if not pathlib.Path(models_dir).is_dir():
                raise ValueError(f"Model configuration at path {path} is not a directory")
            
            # Only attach models actually used in tags, methods, and subnodes
            for model in cfg.models_used:
                model_path = models_dir / model
                if not pathlib.Path(model_path).exists() or pathlib.Path(model_path).is_dir():
                    raise ValueError(f"Model configuration file at path {model_path} is not found")

                with open(model_path, "r") as model_file:
                    raw_model = json5.load(model_file)
                
                cfg.meta.models.append(cfg._build_data_model_config(raw_model))
            
        return cfg

    def _build_data_item_config(self, cfg: Dict[str, Any]) -> DataItemConfig:
        # path, alias, is_list, oneof{model, base}, props
        # TODO: Add unique int alias to every data item 
        item = DataItemConfig()
        item.path = cfg['path']
        item.is_list = isinstance(cfg.get('type'), str) and cfg['type'].startswith('list[')
        type_str = cfg['type']

        # Unwrap list[...] if present
        inner = type_str[5:-1] if item.is_list else type_str

        if inner == 'model':
            self.models_used.add(cfg['model_path'])
            item.model.model_path = cfg['model_path']
            item.model.model_version = cfg.get('model_version', self._default_model_version(cfg['model_path']))
        else:
            item.base = self._map_base_type(inner)

        # Attach any props
        for k, v in cfg.get('props', {}).items():
            item.props.append(self._build_prop(k, v))

        return item

    def _build_data_model_config(self, cfg: Dict[str, Any]) -> DataModelConfig:
        dm = DataModelConfig()
        dm.path = cfg['path']
        dm.version = cfg['version']
        for itm in cfg.get('items', []):
            dm.items.append(self._build_data_item_config(itm))
        for k, v in cfg.get('props', {}).items():
            dm.props.append(self._build_prop(k, v))
        return dm

    def _build_method_config(self, cfg: Dict[str, Any]) -> MethodConfig:
        mc = MethodConfig()
        mc.path = cfg['path']
        for p in cfg.get('params', []):
            mc.params.append(self._build_data_item_config(p))
        for r in cfg.get('responses', []):
            mc.responses.append(self._build_response_config(r))
        # Attach any props
        for k, v in cfg.get('props', {}).items():
            mc.props.append(self._build_prop(k, v))
        return mc

    def _build_response_config(self, cfg: Dict[str, Any]) -> ResponseConfig:
        rc = ResponseConfig()
        rc.code = cfg['code']
        rc.type = config_pb2.ResponseType.Value(cfg['type'].upper())
        for b in cfg.get('body', []):
            rc.body.append(self._build_data_item_config(b))
        for k, v in cfg.get('props', {}).items():
            rc.props.append(self._build_prop(k, v))
        return rc

    def _build_subnode_config(self, cfg: Dict[str, Any]) -> SubnodeConfig:
        sn = SubnodeConfig()
        sn.path = cfg['path']
        for t in cfg.get('tags', []):
            sn.tags.append(self._build_data_item_config(t))
        for m in cfg.get('methods', []):
            sn.methods.append(self._build_method_config(m))
        for s in cfg.get('subnodes', []):
            sn.subnodes.append(self._build_subnode_config(s))
        for k, v in cfg.get('props', {}).items():
            sn.props.append(self._build_prop(k, v))
    

        return sn

    def _build_prop(self, key: str, val: Any) -> Prop:
        p = Prop()
        p.key = key
        # TODO: Support all basedata types (except int, that will always map to long most likely)
        p.type = BaseType.STRING
        p.value.string_data = str(val)
        return p

    def _map_base_type(self, name: str) -> BaseType:
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

    def _default_model_version(self, model_path: str) -> int:
        # TODO: scan model directory to pick latest version
        return 1
