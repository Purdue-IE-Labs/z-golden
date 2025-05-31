import pytest
import zgold as zg 
import pathlib
import time
import random

class TestNodeConfig():
    def test_json_load(self):
        here = pathlib.Path(__file__).parent / "basic_node.json5"
        config = zg.NodeConfig.from_json5(str(here))
        ip_address = "localhost"
        with zg.connect(config, ip_address) as session:
            pass
        