from .node.config import NodeConfig
from .node.session import NodeSession
from .node.comm import Comm


def connect(config: NodeConfig, *router_links: str) -> NodeSession:
    links = list(router_links)
    if len(links) == 0:
        raise ValueError("Must provide at least one router link to connect to")

    for link in links:
        # validate that link starts with tcp/ or quic/ 
        pass
    
    return NodeSession(config, Comm(links))
    
