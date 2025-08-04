import json
import logging
import zenoh
import base64

from zgold.proto import config_pb2
Meta = config_pb2.Meta

ProtoMessage = Meta #| Other Things

logger = logging.getLogger(__name__)

class Comm:
    def __init__(self, links: list[str]):
        config = json.dumps({
            "mode": "client",
            "connect": {
                "endpoints": links,
                "timeout_ms": 3 * 1000,
                "exit_on_failure": True
            }
        })
        self.config = config
        self.links = links
        self._metas: dict[str, bytes] = {}

    def connect(self):
        self.__enter__()
    
    def __enter__(self):
        # logger.debug(f"Attempting to connect to: {self.links}")
        z_config = zenoh.Config.from_json5(self.config)
        session = zenoh.open(z_config)
        # TODO: Log connection status
        self.session = session
        return self

    def __exit__(self, *exc):
        self.session.close()

    def send_meta(self, key: str, meta: Meta):
        self._send_proto(key, meta)

    def _send_proto(self, key: str, value: ProtoMessage):
        # Seriealize
        b = value.SerializeToString()
        b = base64.b64encode(b)

        if isinstance(value, Meta):
            self._metas[key] = b

            def _meta_handler(query: zenoh.Query):
                query.reply(
                    key_expr=key,
                    payload=self._metas[key],
                    encoding="application/protobuf")
            
            self.session.declare_queryable(key, _meta_handler)

        self.session.put(key, b, encoding="application/protobuf")
    