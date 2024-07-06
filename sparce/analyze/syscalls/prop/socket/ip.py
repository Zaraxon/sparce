from aenum import extend_enum
import re

from .....record.prop import PropertyConstructionError

from ...flag.socket import socket

from ...struct.socket import sockaddr_in as sockaddr_in_stru
from ...struct.socket.ip import in_addr_t

from ..common import IntorIntFlag, buffer
from .common import htons

def inet_addr(s: str) -> bytes:
    m = re.search(r'inet_addr\((?P<inet_addr>".*?")\)', s)
    if m is None:
        raise PropertyConstructionError(f'error constructing inet_addr, errdata: {s}')
    return buffer(m.group('inet_addr'))
    
def inet_pton(s: str) -> bytes:
    inet_pton = r'inet_pton\((AF_INET|AF_INET6),\s*(?P<inet_pton>.".*?")(,\s*.*?)?\)'
    m = re.search(inet_pton.format(inet_pton), s)
    if m is None:
        raise PropertyConstructionError(f'err on constructing inet_pton: {s}')
    return buffer(m.group('inet_pton'))

def sockaddr_in(arguments: list) -> sockaddr_in_stru:

    # sin_family
    try:
        if IntorIntFlag(arguments[0][1], socket.Domain) != socket.Domain.AF_INET:
            raise PropertyConstructionError(f'error constructing sockaddr_in.sin_family, errdata: {arguments[0][1]}')
        sin_family = socket.Domain.AF_INET
        
        # sin_port
        sin_port = htons(arguments[1][1])
        
        # sin_addr
        sin_addr = inet_addr(arguments[2][1])

        return sockaddr_in_stru((sin_family, sin_port, in_addr_t([sin_addr])))
    
    except:
        raise PropertyConstructionError(f'error constructing sockaddr_in, errdata: {arguments}')