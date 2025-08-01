import json5
from typing import Any, Dict, Self
import pathlib
import re

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
        self.alias_index: int = 1  
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

        # Modelsa
        # TODO: Validate that model path is a valid zenoh key (no wildcards) - only standard characters and "/" for topic"
        if len(cfg.models_used) > 0 :
            if not pathlib.Path(models_dir).exists():
                raise ValueError(f"Model configuration at path {path} does not exist")
            if not pathlib.Path(models_dir).is_dir():
                raise ValueError(f"Model configuration at path {path} is not a directory")
            
            # Only attach models actually used in tags, methods, and subnodes
            # changed from cfg.models_used to cfg.models_used.copy() since if there's a nested model it throws a runtime error but .copy() removes that issue
            for model in cfg.models_used.copy():
                model_path = pathlib.Path(f"{models_dir}\{model}.json5")
                if not model_path.exists() or model_path.is_dir():
                    raise ValueError(f"Model configuration file at path {str(model_path)} is not found")

                with open(model_path, "r") as model_file:
                    raw_model = json5.load(model_file)
                
                cfg.meta.models.append(cfg._build_data_model_config(raw_model))
                
        return cfg

    def _build_data_item_config(self, cfg: Dict[str, Any]) -> DataItemConfig:
        # path, alias, is_list, oneof{model, base}, props
        # TODO: Add unique int alias to every data item 
        item = DataItemConfig()
        item.path = cfg['path']
        self.test_input(item.path)

        item.is_list = isinstance(cfg.get('type'), str) and cfg['type'].startswith('list[')
        type_str = cfg['type']

        # Unwrap list[...] if present
        inner = type_str[5:-1] if item.is_list else type_str

        if inner == 'model':
            self.models_used.add(cfg['model_path'])
            item.model.model_path = cfg['model_path']
            if re.search(r"[^A-Za-z0-9/_\-.]", item.model.model_path) is not None:
                raise ValueError(f"{item.model.model_path} contains a non alpha-numerical character")
            item.model.model_version = cfg.get('model_version', self._default_model_version(cfg['model_path']))
        else:
            item.base = self._map_base_type(inner)

        # Attach any props
        for k, v in cfg.get('props', {}).items():
            item.props.append(self._build_prop(k, v))

        # Assign unique alias to each data item 
        item.alias = self.alias_index
        self.alias_index += 1

        return item

    def _build_data_model_config(self, cfg: Dict[str, Any]) -> DataModelConfig:
        dm = DataModelConfig()
        dm.path = cfg['path']
        self.test_input(dm.path)

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
    
    def test_input(self, key: str):
        if key == "":
            raise ValueError("Invalid Data Item: Key cannot be empty")
        keyParts = key.split("/")
        for part in keyParts:
            # Keyword Tests
            self.keyword_tests(part)

            # Naming Tests
            self.format_test(part)

    def keyword_tests(self, key: str):
        zenohKeywords = ["STATE", "LINK", "TAGS"]
        self.list_test(key, zenohKeywords)
        
        sharedKeywords = [
            "abstract", "and", "assert", "auto", "boolean", 
            "break", "byte", "case", "catch", "char", 
            "class", "const", "continue", "default", "delete", 
            "do", "double", "else", "enum", "extends", 
            "false", "final", "finally", "float", "for", 
            "goto", "if", "implements", "import", "in", 
            "instanceof", "int", "interface", "long", "native", 
            "new", "not", "null", "or", "package", 
            "private", "protected", "public", "return", "short", 
            "signed", "sizeof", "static", "struct", "super", 
            "switch", "synchronized", "this", "throw", "transient", 
            "true", "try", "typedef", "union", "unsigned", "var", 
            "void", "volatile", "while", "with", "yield"
        ]
        self.list_test(key, sharedKeywords)

        pythonKeywords = [ 
            "as", "def", "del", "elif", "except", "from", "global", "is", "lambda", "None", "nonlocal", "pass", "raise"
        ]
        self.list_test(key, pythonKeywords)

        javaKeywords = [
             "exports",  "module", "requires", "strictfp"
        ]
        self.list_test(key, javaKeywords)

        javaScriptKeywords = [
            "arguments", "await", "debugger", "eval", "export", "function","let", "throws", "typeof",
        ]
        self.list_test(key, javaScriptKeywords)

        cKeywords = [
            "extern", "register"
        ]
        self.list_test(key, cKeywords)

        cPlusPlusKeywords = [
            "and_eq", "bitand", "bitor", "bool", "compl", "friend", "namespace", "not_eq", "or_eq", "template", "using", "virtual", "xor", "xor_eq"
        ]
        self.list_test(key, cPlusPlusKeywords)

        goKeywords = [
            "chan", "defer", "fallthrough", "func", "go", "map", "range", "select", "type",
        ]
        self.list_test(key, goKeywords)

        SQLKeywords = [
            "ADD", "ADD CONSTRAINT", "ALL", "ALTER", "ALTER COLUMN",
            "ALTER TABLE", "ANY", "AS", "ASC",
            "BACKUP DATABASE", "BETWEEN", "CHECK", "COLUMN",
            "CONSTRAINT", "CREATE", "CREATE DATABASE", "CREATE INDEX", "CREATE OR REPLACE VIEW",
            "CREATE TABLE", "CREATE PROCEDURE", "CREATE UNIQUE INDEX", "CREATE VIEW", "DATABASE",
            "DESC", "DISTINCT", "DROP", 
            "DROP COLUMN", "DROP CONSTRAINT", "DROP DATABASE", "DROP DEFAULT", "DROP INDEX",
            "DROP TABLE", "DROP VIEW", "EXEC", "EXISTS", "FOREIGN KEY", 
            "FROM", "FULL OUTER JOIN", "GROUP BY", "HAVING",
            "INDEX", "INNER JOIN", "INNER INTO", "INNER INTO SELECT", "IS NULL",
            "IS NOT NULL", "JOIN", "LEFT JOIN", "LIKE", "LIMIT", 
            "NOT NULL", "ORDER BY", "OUTER JOIN",
            "PRIMARY KEY", "PROCEDURE", "RIGHT JOIN", "ROWNUM", "SELECT",
            "SELECT DISTINCT", "SELECT INTO", "SELECT TOP", "SET", "TABLE",
            "TOP", "TRUNCATE TABLE", "UNOIN ALL", "UNIQUE",
            "UPDATE", "VALUES", "VIEW", "WHERE"
        ]
        self.list_test(key, SQLKeywords)

    def list_test(self, key: str, list: list[str]):
        for compKey in list:
            if key == compKey:
                raise ValueError(f"Invalid Data Item: '{key}' is a reserved keyword")
            
    def format_test(self, key: str):
        # First character cannot be a number
        if (re.search(r"[0-9]", key[0]) is not None):
            raise ValueError(f"Invalid Data Item: {key} may not start with a number")
        
        # Python Convention, can only contain A-z, 0-9, and _ (more strict than others)
        if re.search(r"[^A-Za-z0-9_]", key) is not None:
            raise ValueError(f"Invalid Data Item: {key} may only contain A-Z, a-z, and _")
        
        # C++ Convention, variable names can range from 1 to 255
        if len(key) > 255:
            raise ValueError(f"Invalid Data Item: {key[0:255]}... is too long")
        
