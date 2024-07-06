import re

from .....record.prop import PropertyConstructionError

from ...struct.socket.ipv6 import in6_addr_t
from ...struct.socket.ipv6 import sockaddr_in6 as sockaddr_in6_stru

from ...flag.socket import socket

from ..common import IntorIntFlag
from .common import htonl, htons
from .ip import inet_pton


def sockaddr_in6(arguments: list) -> sockaddr_in6_stru:
    try:
        # sin6_family
        if IntorIntFlag(arguments[0][1], socket.Domain) != socket.Domain.AF_INET6:
            raise PropertyConstructionError(f'error constructing sockaddr_in6.sin6_family, errdata: {arguments[0][1]}')
        sin6_family = socket.Domain.AF_INET6
        # sin6_port
        sin6_port = htons(arguments[1][1])
        # sin6_flowinfo
        sin6_flowinfo = htonl(arguments[1][2])
        # sin6_addr
        sin6_addr = in6_addr_t([inet_pton(arguments[1][3])])
        # sin6_scope_id
        sin6_scope_id = int(arguments[1][4])

        return sockaddr_in6_stru((sin6_family, sin6_port, sin6_flowinfo, sin6_addr, sin6_scope_id))
    
    except:
        raise PropertyConstructionError(f'error constructing sockaddr_in6, errdata: {arguments}')
    