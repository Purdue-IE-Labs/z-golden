import pytest
import zgold as zg 
import pathlib
import time
import random

class TestNodeConfig():
    def test_json_load(self):
        here = pathlib.Path(__file__).parent 
        json_config = here / "basic_node.json5"
        models_dir = here / "my_models"
        config = zg.NodeConfig.from_json5(str(json_config), models_dir=str(models_dir))
        ip_address = "localhost"
        with zg.connect(config, ip_address) as session:
            pass
        