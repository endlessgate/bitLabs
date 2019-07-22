
from labs.net.factories import BaseFactory
from labs.net.peers.tunnel import Tunnel


class AgillaTunnel(Tunnel):
    pass


class AgillaFactory(BaseFactory):
    peer_class = None
    tunnel_class = AgillaTunnel

    def make_peer(self, **kwargs):
        pass

    def make_tunnel(self, **kwargs):
        pass

