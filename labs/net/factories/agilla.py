
from labs.net.factories import BaseFactory


class AgillaFactory(BaseFactory):

    @property
    def node_class(self):
        pass

    @property
    def tunnel_class(self):
        pass

    def build_node(self, **kwargs):
        pass

    def build_tunnel(self, **kwargs):
        pass

