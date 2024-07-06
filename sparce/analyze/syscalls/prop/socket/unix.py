from .....record.prop import PropertyConstructionError

from ...struct.socket import sockaddr_un as sockaddr_un_stru
from ...flag.socket import socket

from ..common import buffer, IntorIntFlag

def sockaddr_un(arguments: list) -> sockaddr_un_stru:
    try:
        # nl_family
        if IntorIntFlag(arguments[0][1], socket.Domain) != socket.Domain.AF_NETLINK:
            raise PropertyConstructionError(f'error constructing sockaddr_in6.sin6_family, errdata: {arguments[0][1]}')
        sun_family = socket.Domain.AF_NETLINK
        # sun_path
        if arguments[1][1][0] == '@':
            sun_path = buffer(arguments[1][1][1:])
        else:
            sun_path = buffer(arguments[1][1])
        return sockaddr_un_stru((sun_family, sun_path))
    except:
        raise PropertyConstructionError(f'error constructing sockaddr_un.sun_path, errdata: {arguments}')