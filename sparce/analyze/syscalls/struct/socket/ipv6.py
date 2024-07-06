from .sockaddr import sockaddr
from ...flag.socket import socket

class in6_addr_t(tuple):

    @property
    def s6_addr(self):
        return self[0]

class sockaddr_in6(sockaddr):

    @property
    def sin6_family(self) -> socket.Domain:
        return self[0]
    @property
    def sin6_port(self) -> int:
        return self[1]
    @property
    def sin6_flowinfo(self) -> int:
        return self[2]
    @property
    def sin6_addr(self) -> in6_addr_t:
        return self[3][0]
    @property
    def sin6_scope_id(self) -> int:
        return self[4]
