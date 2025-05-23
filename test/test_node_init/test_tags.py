import pytest
import zgold as zg 
import pathlib
import time
import random

class TestTags():
    def test_a(self):
        here = pathlib.Path(__file__).parent / "basic_node.json5"
        config = zg.NodeConfig.from_json5(str(here))
        ip_address = "localhost"
        
        with zg.connect(config, ip_address) as session:
            while True:
                # here, we update a base tag on the node with a 
                # value that must match the 'base_type' in the json
                # which in this case is a float
                session.update_tag("base/tag", random.randint(0, 9))
                time.sleep(1)

                # here, we update a nested tag that is in a model
                # 'model/tag' is the name of the tag on the node,
                # but that tag is of type 'model', so we cannot write 
                # to it. We can only write to base tags.
                # Thus, we access item 'baz' which is on 
                # the 'bar' model, of which 'model/tag' is a type
                # Thus, the situation looks similar to this (could be future syntax)
                # model/tag: {
                #   baz: True
                # }
                session.update_tag("model/tag/baz", True)
                time.sleep(1)

    def test_timestamps(self):
