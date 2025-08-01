import json
import logging
import zenoh

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

    def __enter__(self):
        # logger.debug(f"Attempting to connect to: {self.links}")
        z_config = zenoh.Config.from_json5(self.config)
        session = zenoh.open(z_config)
        # TODO: Log connection status
        self.session = session
        return self

    def __exit__(self, *exc):
        self.session.close()