

class Secret:

    def __init__(self, aes, mac, req_mac, resp_mac):
        self._mac_secret = mac
        self._aes_secret = aes
        self._req_cipher = req_mac
        self._resp_cipher = resp_mac

    def request_digest(self):
        pass

    def response_digest(self):
        pass

    def refresh(self, req_mac, resp_mac):
        self._req_cipher = req_mac
        self._resp_cipher = resp_mac



