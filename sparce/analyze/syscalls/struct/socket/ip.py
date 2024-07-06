from .sockaddr import sockaddr
from ...flag.socket import socket

class in_addr_t(tuple):

    @property
    def s_addr(self):
        return self[0]
        
class sockaddr_in(sockaddr):

    @property
    def sin_family(self) -> socket.Domain:
        return self[0]
    @property
    def sin_port(self) -> int:
        return self[1]
    @property
    def sin_addr(self) -> in_addr_t:
        return self[2][0]
