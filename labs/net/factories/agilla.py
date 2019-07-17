
from labs.net.factories import BaseFactory


class AgillaFactory(BaseFactory):

    @property
    def nodeclass(self):
        pass

    @property
    def tunnelclass(self):
        pass

    def build_node(self, **kwargs):
        pass

    def build_tunnel(self, **kwargs):
        pass

