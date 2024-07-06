from ....record.prop import Property, PropertyConstructionError
from .common import buffer, BufferPropertyError
from .common import IntorIntFlag

"""
    syscall constructors
"""

### open
class __open:
    @staticmethod
    def filename(arguments: list) -> bytes:
        return buffer(arguments[0][1])
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)
    
OpenProperties = Property([
    ("arguments", "filename", __open.filename),
    ('retval', 'retval', __open.retval)
])

### read
class __read:
    @staticmethod
    def fd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def buf(arguments: list) -> bytes:
        return buffer(arguments[1][1])
    
    @staticmethod
    def count(arguments: list) -> int:
        return int(arguments[2][1])
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)
    
ReadProperties = Property([
    ("arguments", "fd", __read.fd),
    ('retval', 'retval', __read.retval),
    ('arguments', 'buf', __read.buf),
    ('arguments', 'count', __read.count)
])

### write
class __write:
    @staticmethod
    def fd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def buf(arguments: list) -> bytes:
        return buffer(arguments[1][1])
    
    @staticmethod
    def count(arguments: list) -> int:
        return int(arguments[2][1])
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)
    
WriteProperties = Property([
    ("arguments", "fd", __write.fd),
    ('retval', 'retval', __write.retval),
    ('arguments', 'buf', __write.buf),
    ('arguments', 'count', __write.count)
])

### close
class __close:
    @staticmethod
    def fd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)
    
CloseProperties = Property([
    ("arguments", "fd", __close.fd),
    ('retval', 'retval', __close.retval)
])

### socket
from ..flag.socket import socket
from ..flag.socket.ip import IPProtocol, IntFlag
from ..flag.socket.ipv6 import IPv6Protocol
from ..flag.socket.netlink import NetLinkFamily
class __socket:

    @staticmethod
    def domain(arguments: list) -> socket.Domain:
        return IntorIntFlag(arguments[0][1], socket.Domain)
    
    @staticmethod
    def type(arguments: list) -> socket.Type:
        return IntorIntFlag(arguments[1][1], socket.Domain)
        
    @staticmethod   
    def protocol(arguments: list) -> IPProtocol | IPv6Protocol | NetLinkFamily:

        if IntorIntFlag(arguments[0][1], socket.Domain) == socket.Domain.AF_INET:
            return IntorIntFlag(arguments[2][1], IPProtocol)
        if IntorIntFlag(arguments[0][1], socket.Domain) == socket.Domain.AF_INET6:
            return IntorIntFlag(arguments[2][1], IPv6Protocol)
        if IntorIntFlag(arguments[0][1], socket.Domain) == socket.Domain.AF_UNIX:
            return IntorIntFlag(arguments[2][1], IntFlag)
        if IntorIntFlag(arguments[0][1], socket.Domain) == socket.Domain.AF_NETLINK:
            return IntorIntFlag(arguments[2][1], NetLinkFamily)
        
        raise PropertyConstructionError('unknown')
    
    @staticmethod   
    def retval(retval: str) -> int:
        return int(retval)  
    
SocketProperties = Property([
    ("arguments", "domain", __socket.domain),
    ("arguments", "type", __socket.type),
    ("arguments", "protocol", __socket.protocol),
    ('retval', 'retval', __socket.retval)
])

### connect
from ..flag.socket import socket
from .socket.ip import sockaddr_in, sockaddr_in_stru
from .socket.ipv6 import sockaddr_in6, sockaddr_in6_stru
from .socket.netlink import sockaddr_nl, sockaddr_nl_stru
from .socket.unix import sockaddr_un, sockaddr_un_stru
import re
class __connect:
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def addr(arguments: list) -> sockaddr_in_stru | sockaddr_un_stru | sockaddr_in6_stru | sockaddr_nl_stru: 
        constructors = [sockaddr_in, sockaddr_in6, sockaddr_un, sockaddr_nl]
        for constructor in constructors:
            try:
                return constructor(arguments[1][1])
            except PropertyConstructionError:
                pass
        raise PropertyConstructionError(f'unknown connect addr, errdata: {arguments[1][1]}')

    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

ConnectProperties = SocketProperties = Property([
    ("arguments", "sockfd", __connect.sockfd),
    ("arguments", "addr", __connect.addr),
    ("retval", "retval", __connect.retval),
])

### bind
from ..flag.socket import socket
from ..struct.socket import sockaddr
from .socket.ip import sockaddr_in, sockaddr_in_stru
from .socket.ipv6 import sockaddr_in6, sockaddr_in6_stru
from .socket.netlink import sockaddr_nl, sockaddr_nl_stru
from .socket.unix import sockaddr_un, sockaddr_un_stru
import re
class __bind:
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def addr(arguments: list) -> sockaddr: 
        constructors = [sockaddr_in, sockaddr_in6, sockaddr_un, sockaddr_nl]
        for constructor in constructors:
            try:
                return constructor(arguments[1][1])
            except PropertyConstructionError:
                pass
        raise PropertyConstructionError(f'unknown connect addr, errdata: {arguments[1][1]}')
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)
BindProperties = SocketProperties = Property([
    ("arguments", "sockfd", __bind.sockfd),
    ("arguments", "addr", __bind.addr),
    ("retval", "retval", __bind.retval),
])


### listen
class __listen:
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])

    @staticmethod
    def backlog(arguments: list) -> int:
        return int(arguments[1][1])
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

ListenProperties = Property([
    ("arguments", "sockfd", __listen.sockfd),
    ("arguments", "backlog", __listen.backlog),
    ("retval", "retval", __listen.retval),
    ])


### accept
from ..flag.socket import socket
from ..struct.socket import sockaddr
from .socket.ip import sockaddr_in, sockaddr_in_stru
from .socket.ipv6 import sockaddr_in6, sockaddr_in6_stru
from .socket.netlink import sockaddr_nl, sockaddr_nl_stru
from .socket.unix import sockaddr_un, sockaddr_un_stru
class __accept:
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def addr(arguments: list) -> sockaddr: 
        constructors = [sockaddr_in, sockaddr_in6, sockaddr_un, sockaddr_nl]
        for constructor in constructors:
            try:
                return constructor(arguments[1][1])
            except PropertyConstructionError:
                pass
        raise PropertyConstructionError(f'unknown connect addr, errdata: {arguments[1][1]}')
     
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

AcceptProperties = Property([
    ('arguments', 'sockfd', __accept.sockfd),
    ('arguments', 'addr', __accept.addr),
    ('retval', 'retval', __accept.retval)
    ])

### send 
"""
    ssize_t send(int sockfd, const void buf[.len], size_t len, int flags);
"""
from ..flag.send import SendFlag
class __send:
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def buf(arguments: list) -> bytes:
        try:
            return buffer(arguments[1][1])
        except BufferPropertyError:
            raise RuntimeError(f'err on constructing read.buf, errdata {arguments[1][1]}')

    @staticmethod
    def len(arguments: str) -> int:
        return int(arguments[2][1])
    
    @staticmethod
    def flags(arguments: list) -> int|SendFlag:
        return IntorIntFlag(arguments[3][1], SendFlag)
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

SendProperties = Property([
    ('arguments', 'sockfd', __send.sockfd),
    ('arguments', 'buf', __send.buf),
    ('arguments', 'len', __send.len),
    ('arguments', 'flags', __send.flags),
    ('retval', 'retval', __send.retval)
])

### recv
"""
ssize_t recv(int sockfd, void buf[.len], size_t len,
                        int flags);
"""
from ..flag.recv import RecvFlag
class __recv:
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def buf(arguments: list) -> bytes:
        return buffer(arguments[1][1])

    @staticmethod
    def len(arguments: list) -> int:
        return int(arguments[2][1])
    
    @staticmethod
    def flags(arguments: list) -> int|RecvFlag:
        return IntorIntFlag(arguments[3][1], RecvFlag)

    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

RecvProperties = Property([
    ('arguments', 'sockfd', __recv.sockfd),
    ('arguments', 'buf', __recv.buf),
    ('arguments', 'len', __recv.len),
    ('arguments', 'flags', __recv.flags),
    ('retval', 'retval', __recv.retval)
])

from ..struct.iovec import iovec
class __readv:

    @staticmethod
    def fd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def iov(arguments: list) -> tuple[iovec]:
        iovecs_data = arguments[1][1]
        return tuple([
            (buffer(iov[0][1]), int(iov[1][1])) for _, iov in iovecs_data
        ])
            
    @staticmethod
    def iovcnt(arguments: list) -> int:
        return int(arguments[2][1])
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

ReadvProperties = Property([
    ('arguments', 'fd', __readv.fd),
    ('arguments', 'iov', __readv.iov),
    ('arguments', 'iovcnt', __readv.iovcnt),
    ('retval', 'retval', __readv.retval)  
])

from ..struct.iovec import iovec as iovec_stru
from .iovec import iovec, iovec_stru
class __writev:

    @staticmethod
    def fd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def iov(arguments: list) -> tuple[iovec]:
        iovecs_data = arguments[1][1]
        return tuple([
            iovec_stru(iov) for _, iov in iovecs_data
        ])
            
    @staticmethod
    def iovcnt(arguments: list) -> int:
        return int(arguments[2][1])
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

WritevProperties = Property([
    ('arguments', 'fd', __writev.fd),
    ('arguments', 'iov', __writev.iov),
    ('arguments', 'iovcnt', __writev.iovcnt),
    ('retval', 'retval', __writev.retval)  
])

"""
    ssize_t sendmsg(int socket, const struct msghdr *message, int flags);
"""
from typing import Any
from ..flag.socket import socket
from ..struct.socket import sockaddr
from .socket.ip import sockaddr_in, sockaddr_in_stru
from .socket.ipv6 import sockaddr_in6, sockaddr_in6_stru
from .socket.netlink import sockaddr_nl, sockaddr_nl_stru
from .socket.unix import sockaddr_un, sockaddr_un_stru
"""
    ssize_t sendto(int sockfd ，const void buf [. len ]，size_t len ，int flags ，
                    const struct sockaddr * dest_addr ，socklen_t addrlen ); 
"""
class __sendto:
    
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def buf(arguments: list) -> bytes | Any:
        
        constructors = [buffer, ]
        for constructor in constructors:
            try:
                return constructor(arguments[1][1])
            except PropertyConstructionError:
                pass

        print(f'WARNING: failed constructing sendto buf. remains raw format: {arguments[1][1]}')
        return arguments[1][1]
        
    
    @staticmethod
    def len(arguments: list) -> int:
        return int(arguments[2][1])
    
    @staticmethod
    def flags(arguments: list) -> int|SendFlag:
        return IntorIntFlag(arguments[3][1], SendFlag)
    
    @staticmethod
    def dest_addr(arguments: list) -> sockaddr: 
        constructors = [sockaddr_in, sockaddr_in6, sockaddr_un, sockaddr_nl]
        
        if arguments[4][1] == 'NULL':
            return None
        
        for constructor in constructors:
            try:
                return constructor(arguments[4][1])
            except PropertyConstructionError:
                pass
        raise PropertyConstructionError(f'unknown sendto dest_addr, errdata: {arguments[4][1]}')
    
    @staticmethod
    def addrlen(arguments: list) -> int:
        return int(arguments[5][1])
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

SendToProperties = Property([
    ('arguments', 'sockfd', __sendto.sockfd),
    ('arguments', 'buf', __sendto.buf),
    ('arguments', 'len', __sendto.len),
    ('arguments', 'flags', __sendto.flags),
    ('arguments', 'dest_addr', __sendto.dest_addr),
    ('arguments', 'addrlen', __sendto.addrlen),
    ('retval', 'retval', __sendto.retval),
])

"""
    ssize_t recvfrom(int socket, void *restrict buffer, size_t length,
        int flags, struct sockaddr *restrict address,
        socklen_t *restrict address_len);
"""
class __recvfrom:
    
    @staticmethod
    def socket(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def buffer(arguments: list) -> bytes | Any:
        
        constructors = [buffer, ]
        for constructor in constructors:
            try:
                return constructor(arguments[1][1])
            except PropertyConstructionError:
                pass

        print(f'WARNING: failed constructing recvfrom buf. remains raw format: {arguments[1][1]}')
        arguments[1][1]
        
    
    @staticmethod
    def length(arguments: list) -> int:
        return int(arguments[2][1])
    
    @staticmethod
    def flags(arguments: list) -> int|SendFlag:
        return IntorIntFlag(arguments[3][1], SendFlag)
    
    @staticmethod
    def address(arguments: list) -> sockaddr: 
        constructors = [sockaddr_in, sockaddr_in6, sockaddr_un, sockaddr_nl]
        for constructor in constructors:
            try:
                return constructor(arguments[4][1])
            except PropertyConstructionError:
                pass
        raise PropertyConstructionError(f'unknown recvfrom address, errdata: {arguments[4][1]}')
    
    @staticmethod
    def address_len(arguments: list) -> int:
        try:
            return int(arguments[5][1])
        except TypeError:
            # TODO: 需要更精细的解析, 目前由于arguments解析"[28 => 16]"的时候会以'='切割成[('28 ', '> 16')], 所以有了这个粗糙的构造
            # 但这里真正的修复实际上需要arguments更精细的解析, 目前还做不到.
            return int(re.search(r'\d+', arguments[5][1][0][-1]).group(0), 0)

    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

RecvFromProperties = Property([
    ('arguments', 'socket', __recvfrom.socket),
    ('arguments', 'buffer', __recvfrom.buffer),
    ('arguments', 'length', __recvfrom.length),
    ('arguments', 'flags', __recvfrom.flags),
    ('arguments', 'address', __recvfrom.address),
    ('arguments', 'address_len', __recvfrom.address_len),
    ('retval', 'retval', __recvfrom.retval),  
])

"""
    ssize_t sendmsg(int sockfd, const struct msghdr *msg, int flags);
"""
from ..struct.msghdr import msghdr as msghdr_stru
from .msghdr import msghdr
class __sendmsg:
    
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def msg(arguments: list) -> msghdr_stru:
        return msghdr(arguments[1][1])
    
    @staticmethod
    def flags(arguments: list) -> SendFlag:
        return IntorIntFlag(arguments[2][1], SendFlag)
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

SendMsgProperties = Property([
    ('arguments', 'sockfd', __sendmsg.sockfd),
    ('arguments', 'msg', __sendmsg.msg),
    ('arguments', 'flags', __sendmsg.flags),
    ('retval', 'retval', __sendmsg.retval),  
])

"""
    ssize_t recvmsg(int sockfd, struct msghdr *msg, int flags);
"""
from ..struct.msghdr import msghdr as msghdr_stru
from .msghdr import msghdr
class __recvmsg:
    
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def msg(arguments: list) -> msghdr_stru:
        return msghdr(arguments[1][1])
    
    @staticmethod
    def flags(arguments: list) -> RecvFlag:
        return IntorIntFlag(arguments[2][1], RecvFlag)
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

RecvMsgProperties = Property([
    ('arguments', 'sockfd', __recvmsg.sockfd),
    ('arguments', 'msg', __recvmsg.msg),
    ('arguments', 'flags', __recvmsg.flags),
    ('retval', 'retval', __recvmsg.retval),  
])

"""
       int sendmmsg(int sockfd, struct mmsghdr *msgvec, unsigned int vlen,
                    int flags);
"""
from ..struct.msghdr import mmsghdr as mmsghdr_stru
from .msghdr import mmsghdr
class __sendmmsg:
    
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def msgvec(arguments: list) -> tuple[mmsghdr_stru]:
        return tuple(mmsghdr(_[1]) for _ in arguments[1][1])
    
    @staticmethod
    def vlen(arguments: list) -> int:
        return int(arguments[2][1], 0)
    
    @staticmethod
    def flags(arguments: list) -> SendFlag:
        return IntorIntFlag(arguments[3][1], SendFlag)
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

SendMMsgProperties = Property([
    ('arguments', 'sockfd', __sendmmsg.sockfd),
    ('arguments', 'msgvec', __sendmmsg.msgvec),
    ('arguments', 'vlen', __sendmmsg.vlen),
    ('arguments', 'flags', __sendmmsg.flags),
    ('retval', 'retval', __sendmmsg.retval),  
])

"""
       int recvmmsg(int sockfd, struct mmsghdr *msgvec, unsigned int vlen,
                    int flags, struct timespec *timeout);
"""
from ..struct.msghdr import mmsghdr as mmsghdr_stru
from .msghdr import mmsghdr
class __recvmmsg:
    
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def msgvec(arguments: list) -> tuple[mmsghdr_stru]:
        return tuple(mmsghdr(_[1]) for _ in arguments[1][1])
    
    @staticmethod
    def vlen(arguments: list) -> int:
        return int(arguments[2][1], 0)
    
    @staticmethod
    def flags(arguments: list) -> RecvFlag:
        return IntorIntFlag(arguments[3][1], RecvFlag)
    
    @staticmethod
    def timeout(arguments: list) -> None:
        raise NotImplementedError()
    
    @staticmethod
    def retval(retval: str) -> int:
        return int(retval)

RecvMMsgProperties = Property([
    ('arguments', 'sockfd', __recvmmsg.sockfd),
    ('arguments', 'msgvec', __recvmmsg.msgvec),
    ('arguments', 'vlen', __recvmmsg.vlen),
    ('arguments', 'flags', __recvmmsg.flags),
    ('arguments', 'timeout', __recvmmsg.timeout),
    ('retval', 'retval', __recvmmsg.retval),
])

"""
       int dup(int oldfd ); 
       int dup2(int oldfd , int newfd ); 
"""
class __dup:
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def oldfd(arguments: list) -> int:
        return int(arguments[1][1])
    
    @staticmethod
    def retval(retval: str) -> int:
        return retval
    
class __dup2:
    @staticmethod
    def sockfd(arguments: list) -> int:
        return int(arguments[0][1])
    
    @staticmethod
    def oldfd(arguments: list) -> int:
        return int(arguments[1][1])
    
    @staticmethod
    def newfd(arguments: list) -> int:
        return int(arguments[2][1])
    
    @staticmethod
    def retval(retval: str) -> int:
        return retval

DupProperties = Property([
    ('arguments', 'sockfd', __dup.sockfd),
    ('arguments', 'oldfd', __dup.oldfd),
    ('retval', 'retval', __dup.retval),  
])
Dup2Properties = Property([
    ('arguments', 'sockfd', __dup2.sockfd),
    ('arguments', 'oldfd', __dup2.oldfd),
    ('arguments', 'newfd', __dup2.newfd),
    ('retval', 'retval', __dup2.retval),  
])