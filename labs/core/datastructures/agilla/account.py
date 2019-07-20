
from labs.core.datastructures.base import BaseAccount


class Account(BaseAccount):

    def __init__(self,
                 nonce: int = 0,
                 balance: int = 0,
                 access: bytes = b'',
                 storage: bytes = b'',
                 path: bytes = b'',
                 active: list = None):

        super().__init__(nonce, balance, access, storage, path, active or [])


