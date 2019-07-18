
from abc import ABC, abstractmethod
from cancel_token import CancelToken


class BaseFactory(ABC):

    @property
    @abstractmethod
    def node_class(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def tunnel_class(self):
        raise NotImplementedError

    @abstractmethod
    def build_node(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def build_tunnel(self, **kwargs):
        raise NotImplementedError

    def __init__(self, secretkey, token: CancelToken):
        self.secretkey = secretkey
        self.token = token
