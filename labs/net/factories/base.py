
from abc import ABC, abstractmethod
from cancel_token import CancelToken


class BaseFactory(ABC):
    peer_class = None
    tunnel_class = None

    @abstractmethod
    def make_peer(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def make_tunnel(self, **kwargs):
        raise NotImplementedError

    def __init__(self, secretkey, token: CancelToken):
        self.secretkey = secretkey
        self.token = token
