from ...flag.socket import socket
from .sockaddr import sockaddr

class sockaddr_un(sockaddr):

    @property
    def sun_family(self) -> socket.Domain:
        return self[0]
    @property
    def sun_path(self) -> bytes:
        return self[1]