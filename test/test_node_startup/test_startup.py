import pytest
import zgold as zg 
import pathlib
import time
import random
import base64

from zgold.proto import config_pb2
Meta = config_pb2.Meta

class TestNodeConfig():

    @pytest.mark.parametrize("json_file", [
        ("json_files\\basic_node.json5"),
        # ("json_files\\tag_node.json5"),
        # ("json_files\\method_node.json5"),
        # ("json_files\\oops_all_models.json5"),
        # ("json_files\\just_key.json5"),
        # ("json_files\\nested_model.json5"),
    ])
    def test_json_load(self, json_file):
        here = pathlib.Path(__file__).parent 
        json_config = here / json_file
        models_dir = here / "my_models"
        config = zg.NodeConfig.from_json5(str(json_config), models_dir=str(models_dir))
        # print(config.meta)
        router_link1 = "tcp/[::1]:7447"
        jonas_router = "tcp/192.168.4.243:7447"
        router_link2 = "localhost:4775"
        with zg.connect(config, router_link1) as session:
            result = session._comm.session.get(config.meta_key).recv()

            assert result

            print(result.result)

    @pytest.mark.parametrize("json_file", [
        ("json_files\\keyword_error.json5"),
        ("json_files\\format_error_0.json5"),
        ("json_files\\format_error_1.json5"),
        ("json_files\\format_error_2.json5"),
        ("json_files\\format_error_3.json5"),
    ])
    def test_json_load_fail(self, json_file):
        here = pathlib.Path(__file__).parent
        json_config = here / json_file
        models_dir = here / "my_models"
        with pytest.raises(ValueError):
            config = zg.NodeConfig.from_json5(str(json_config), models_dir=str(models_dir))