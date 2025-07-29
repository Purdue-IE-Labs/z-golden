import pytest
import zgold as zg 
import pathlib
import time
import random

class TestNodeConfig():

    @pytest.mark.parametrize("json_file", [
        ("json_files\\basic_node.json5"),
        ("json_files\\tag_node.json5"),
        ("json_files\\method_node.json5"),
        ("json_files\\oops_all_models.json5"),
        ("json_files\\just_key.json5"),
        ("json_files\\nested_model.json5")
    ])
    def test_json_load(self, json_file):
        here = pathlib.Path(__file__).parent 
        json_config = here / json_file
        models_dir = here / "my_models"
        config = zg.NodeConfig.from_json5(str(json_config), models_dir=str(models_dir))
        ip_address = "localhost"
        with zg.connect(config, ip_address) as session:
            pass