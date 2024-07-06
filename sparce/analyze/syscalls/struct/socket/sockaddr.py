from ...flag.socket import socket

class sockaddr(tuple):
    
    @property
    def sa_family(self) -> socket.Domain:
        return self[0]
