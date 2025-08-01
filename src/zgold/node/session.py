from .config import NodeConfig
from .comm import Comm


class NodeSession:
    def __init__(self, config: NodeConfig, comm: Comm):
        self._comm = comm
        self.config = config
        # self.ks = config.ks
        # self.connections: dict[str, RemoteConnection] = dict()

        self._comm.connect()


        # logger.debug

        self._startup()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._comm.__exit__(*exc)

    def _startup(self):
        # TODO: Verify Collision
        # Send Meta
        self._comm.send_meta(self.config.meta_key, self.config.meta)
        # Update State
        
        # Liveliness Token


        # TODO: Method Handler Linking
        pass