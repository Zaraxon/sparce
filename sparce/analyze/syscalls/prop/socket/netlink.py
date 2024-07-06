import re

from .....record.prop import PropertyConstructionError

from ...struct.socket import sockaddr_nl as sockaddr_nl_stru
from ...struct.socket.netlink import nlmsghdr as nlmsghdr_stru
from ...flag.socket.netlink import NlmsgFlag, NlMsgType
from ...flag.socket import socket

from ..common import IntorIntFlag

def sockaddr_nl(arguments: list) -> sockaddr_nl_stru:
    try:
        # nl_family
        if IntorIntFlag(arguments[0][1], socket.Domain) != socket.Domain.AF_NETLINK:
            raise PropertyConstructionError(f'error constructing sockaddr_in6.sin6_family, errdata: {arguments[0][1]}')
        nl_family = socket.Domain.AF_NETLINK
        # nl_pad 在strace中不显示
        assert arguments[1][0] != 'nl_pad'
        # nl_pid
        nl_pid = int(arguments[1][1])
        # nl_groups
        nl_groups = int(arguments[2][1], 0)
        return sockaddr_nl_stru((nl_family, 0, nl_pid, nl_groups))
    except:
        raise PropertyConstructionError(f'error constructing sockaddr_in6.sin6_family, errdata: {arguments}')

def nlmsghdr(arguments: list) -> nlmsghdr_stru:
    # nlmsg_len
    nlmsg_len = int(arguments[0][1])
    # nlmsg_type
    arg = arguments[1][1]
    m = re.search(r'\s*/\*.*?\*/\s*',arg)
    if m is not None:
        arg = arg[:m.start()]+arg[m.end():]
    nlmsg_type = IntorIntFlag(arg, NlMsgType)
    # nlmsg_flags
    nlmsg_flags = IntorIntFlag(arguments[2][1], NlmsgFlag)
    # nlmsg_seq
    nlmsg_seq = int(arguments[3][1], 0)
    # nlmsg_pid
    nlmsg_pid = int(arguments[4][1], 0)

    return nlmsghdr_stru((nlmsg_len, nlmsg_type, nlmsg_flags, nlmsg_seq, nlmsg_pid))
