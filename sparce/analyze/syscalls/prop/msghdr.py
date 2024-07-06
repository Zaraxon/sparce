import re
from ast import literal_eval

from ....record.prop import PropertyConstructionError

from ..struct.msghdr import msghdr as msghdr_stru
from ..struct.msghdr import mmsghdr as mmsghdr_stru

from .socket.unix import sockaddr_un, sockaddr_un_stru
from .socket.netlink import sockaddr_nl, sockaddr_nl_stru
from .socket.ip import sockaddr_in, sockaddr_in_stru
from .socket.ipv6 import sockaddr_in6, sockaddr_in6_stru

from .iovec import iovec, iovec_stru

from .common import buffer

"""
    from https://man7.org/linux/man-pages/man2/sendmsg.2.html

The msg_name field is used on an unconnected socket to specify
       the target address for a datagram.
"""
class MsgHdrIOVBaseError(PropertyConstructionError):
    pass


def msghdr(arguments: list) -> msghdr_stru:
    # msg_name
    msg_name_constructors = [sockaddr_un, sockaddr_in, sockaddr_in6, sockaddr_nl, buffer]
    msg_name_arg = arguments[0][1]
    msg_name = None
    for c in msg_name_constructors:
        try:
            msg_name = c(msg_name_arg)
            break
        except PropertyConstructionError:
            continue

    if msg_name is None:
        if msg_name_arg == 'NULL':
            msg_name = None
        else:
            raise PropertyConstructionError(f"constructing msghdr.msgname: {msg_name_arg}")
    
    # msg_namelen
    try:
        msg_namelen = int(arguments[1][1], 0)
    except ValueError:
        # TODO: 和address_len类似, 这里有"127 => 16"的情况
        if '=>' in arguments[1][1]:
            msg_namelen = int(arguments[1][1].split('=>')[-1], 0)

    # msg_iov
    msg_iovs_arg = arguments[2][1]
    msg_iov = list()
    for _, msg_iov_arg in msg_iovs_arg:
        try:
            _iovec = iovec(msg_iov_arg)
            msg_iov.append(_iovec)
        except PropertyConstructionError:
            print('WARNING: skip constructing msghdr.msg_iov, data:', msg_iov_arg)
            msg_iov.append(msg_iov_arg)
    msg_iov = tuple(msg_iov)

    # msg_iovlen
    msg_iovlen = int(arguments[3][1], 0)

    # msg_control
    pass

    # msg_controllen
    pass

    return msghdr_stru((msg_name, msg_namelen, msg_iov, msg_iovlen))


def mmsghdr(arguments: list) -> mmsghdr_stru:
    # msg_len
    try:
        msg_len = int(arguments[1][1], 0)
    except:
        assert False
    # msg_hdr
    msg_hdr = msghdr(arguments[0][1])
    
    return mmsghdr_stru((msg_len, msg_hdr))

