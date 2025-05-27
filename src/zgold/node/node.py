import pathlib
import json5

from typing import Any

class NodeConfig:
    def __init__(self, key: str):
        self._user_key = key
        self.ks = NodeKeySpace.from_user_key(key)
        self.tag_config = TagConfig({})
        self.methods: dict[str, MethodConfig] = dict()
        self.subnodes: dict[str, SubnodeConfig] = dict()
        self.models: dict[str, DataModelConfig] = dict()

    @classmethod
    def from_json5(cls, path: str):
        '''
        Creates a new node by loading the opening the parameter path with read persmissions to json5 and returns the NodeConfig of the new node
        
        Arguments:
            cls (type[Self@NodeConfig]): The NodeConfig class
            path (str): The path being opened on and loaded into json5

        Returns:
            NodeConfig
        '''
        if not pathlib.Path(path).exists():
            raise ValueError(f"Node configuration at path {path} does not exist")
        if pathlib.Path(path).is_dir():
            raise ValueError(f"Node configuration at path {path} is a directory")
        with open(path, "r") as f:
            node: dict[str, Any] = json5.load(f)
        return cls._config_from_json5_obj(node)
    
    @classmethod
    def from_json5_str(cls, string: str):
        '''
        Creates a new node by loading the parameter string to json5 and returns the NodeConfig of the new node
        
        Arguments:
            cls (type[Self@NodeConfig]): The NodeConfig class
            string (str): The string being directly loaded to json5

        Returns:
            NodeConfig
        '''
        node: dict[str, Any] = json5.loads(string) # type: ignore
        return cls._config_from_json5_obj(node)

    @staticmethod
    def _config_from_json5_obj(obj: dict[str, Any]):
        if "key" not in obj:
            raise LookupError(f"Keyword 'key' not found for node configuration")
        config = NodeConfig(obj["key"])
        config.tag_config = TagConfig.from_json5(obj.get("tags", []), obj.get("writable_config", []), obj.get("group_config", []))

        for method_json in obj.get("methods", []):
            method = MethodConfig.from_json5(method_json)
            config.methods[method.path] = method

        from gedge.node.subnode import SubnodeConfig
        for subnode_json in obj.get("subnodes", []):
            subnode = SubnodeConfig.from_json5(subnode_json, config.ks)
            config.subnodes[subnode.name] = subnode
        
        return config
