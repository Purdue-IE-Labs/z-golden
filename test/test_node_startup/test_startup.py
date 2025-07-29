import pytest
import zgold as zg 
import pathlib
import time
import random

class TestNodeConfig():

    @pytest.mark.parametrize("json_file", [
        ("basic_node.json5"),
        ("tag_node.json5"),
        ("method_node.json5"),
        ("oops_all_models.json5"),
        ("just_key.json5"),
        ("nested_model.json5"),
        ("big_num.json5")
    ])
    def test_json_load(self, json_file):
        here = pathlib.Path(__file__).parent 
        json_config = here / json_file
        models_dir = here / "my_models"
        config = zg.NodeConfig.from_json5(str(json_config), models_dir=str(models_dir))
        ip_address = "localhost"
        with zg.connect(config, ip_address) as session:
            pass