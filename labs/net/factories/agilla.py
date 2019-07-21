
from labs.net.factories import BaseFactory


class AgillaFactory(BaseFactory):

    @property
    def peer_class(self):
        pass

    @property
    def tunnel_class(self):
        pass

    def make_peer(self, **kwargs):
        pass

    def make_tunnel(self, **kwargs):
        pass

