"""
    从一个SyscallRecord[和一个Activity类作为上下文]提取信息.

    这一部分从record的参数里提取出有效内容. 这部分的功能是"内部负责"的.
"""

from dataclasses import dataclass

from typing import Sequence, Collection, Any

from ...record import SyscallRecord
from ...record.types import Structure, Expr

import re

def error_desc(record: SyscallRecord) -> str:
    """
        TODO: 找到更好的方式替代掉在这里写正则
    """
    m = re.match("\s+\([a-zA-Z0-9 ]*?\)\s*$", record.origin_line)
    if m is None:
        return None
    else:
        return m.group(0).strip().lstrip('(').rstrip(')')

def mk_getfds(*_argpos):
    """
        >= 0: arguments[0] 
        -1  : retval
    """
    def getfds(record, action=None, argpos=_argpos):
        fds = []
        for p in argpos:
            if p >= 0 and record.arguments[p] >= 0:
                fds.append(record.arguments[p])
            elif p == -1 and record.retval >= 0:
                fds.append(record.retval)
            else:
                pass
        return tuple(fds)
    return getfds

def selectfds(record, _argpos=0):
    fds = tuple()
    if isinstance(record.arguments[_argpos], Sequence) and \
        not isinstance(record.arguments[_argpos], str):
        fds += tuple([pollfd for pollfd in record.arguments[_argpos]])
    elif isinstance(record.arguments[_argpos], int) or record.arguments[_argpos] == 'NULL':
        fds += tuple()
    else:
        return None
    return fds

class _socket:
    fd = mk_getfds(-1)
class _bind:
    fd = mk_getfds(0)
class _listen:
    fd = mk_getfds(0)
class _accept:
    @staticmethod
    def fd(record:SyscallRecord, action=None):
        fds = {record.arguments[0]}
        if isinstance(record.retval, int) and record.retval >= 0:
            fds.add(record.retval)
        return tuple(fds)
class _connect:
    fd = mk_getfds(0)
class _send:
    fd = mk_getfds(0)
    @staticmethod
    def count(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def buf(record: SyscallRecord, action=None) -> bytes|None:
        if isinstance(record.arguments[1], bytes):
            return record.arguments[1]
class _recv:
    fd = mk_getfds(0)
    @staticmethod
    def count(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def buf(record: SyscallRecord, action=None) -> bytes|None:
        if isinstance(record.arguments[1], bytes):
            return record.arguments[1]
class _sendto:
    fd = mk_getfds(0)
    @staticmethod
    def count(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def buf(record: SyscallRecord, action=None) -> bytes|None:
        if isinstance(record.arguments[1], bytes):
            return record.arguments[1]
class _recvfrom:
    fd = mk_getfds(0)
    @staticmethod
    def count(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def buf(record: SyscallRecord, action=None) -> bytes|None:
        if isinstance(record.arguments[1], bytes):
            return record.arguments[1]
        
class _sendmsg:
    fd = mk_getfds(0)
    @staticmethod
    def count(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def msg(record: SyscallRecord, action=None) -> Structure|None:
        if isinstance(record.arguments[1], Structure):
            return record.arguments[1]

class _sendmmsg:
    fd = mk_getfds(0)
    @staticmethod
    def msgcount(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def msgvec(record: SyscallRecord, action=None) -> Sequence|None:
        if isinstance(record.arguments[1], Sequence):
            for _ in record.arguments[1]:
                if not isinstance(_, Structure):
                    return None
            return record.arguments[1]
        return None
    
class _recvmmsg:
    fd = mk_getfds(0)
    @staticmethod
    def msgcount(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def msgvec(record: SyscallRecord, action=None) -> Sequence|None:
        if isinstance(record.arguments[1], Sequence):
            for _ in record.arguments[1]:
                if not isinstance(_, Structure):
                    return None
            return record.arguments[1]
        return None

class _recvmsg:
    fd = mk_getfds(0)
    @staticmethod
    def count(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def msg(record: SyscallRecord, action=None) -> Structure|None:
        if isinstance(record.arguments[1], Structure):
            return record.arguments[1]
    
class _getsockopt:
    fd = mk_getfds(0)
class _setsockopt:
    fd = mk_getfds(0)
class _getsockname:
    fd = mk_getfds(0)
class _getpeername:
    fd = mk_getfds(0)
class _ioctl:
    fd = mk_getfds(0)
class _poll:
    @staticmethod
    def fd(record: SyscallRecord, action=None) -> Sequence[int]:
        try:
            if isinstance(record.arguments[0], Sequence):
                return tuple([pollfd[0] for pollfd in record.arguments[0]])
            elif isinstance(record.arguments[0], int) or record.arguments[0] == 'NULL':
                return tuple()
            else:
                raise ValueError('_poll:'+str(record.arguments[0]))
        except:
            print('arguments[0]:')
            for pollfd in record.arguments[0]:
                print('pollfd:', pollfd, type(pollfd))
                print('pollfd:', pollfd[0])
class _select:
    @staticmethod
    def fd(record: SyscallRecord, action=None) -> Sequence[int]:
        return selectfds(record, 1) + selectfds(record, 2) + selectfds(record, 3)
class _newselect:
    @staticmethod
    def fd(record: SyscallRecord, action=None) -> Sequence[int]:
        return selectfds(record, 1) + selectfds(record, 2) + selectfds(record, 3)
class _read:
    fd = mk_getfds(0)
    @staticmethod
    def count(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def buf(record: SyscallRecord, action=None) -> bytes|None:
        if isinstance(record.arguments[1], bytes):
            return record.arguments[1]
class _write:
    fd = mk_getfds(0)
    @staticmethod
    def count(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def buf(record: SyscallRecord, action=None) -> bytes|None:
        if isinstance(record.arguments[1], bytes):
            return record.arguments[1]   
class _readv:
    fd = mk_getfds(0)
    @staticmethod
    def count(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def iov(record: SyscallRecord, action=None) -> Sequence|None:
        if isinstance(record.arguments[1], Sequence):
            return record.arguments[1]
class _writev:
    fd = mk_getfds(0)
    @staticmethod
    def count(record: SyscallRecord, action=None) -> int:
        return record.retval if record.retval >= 0 else 0
    @staticmethod
    def iov(record: SyscallRecord, action=None) -> Sequence|None:
        if isinstance(record.arguments[1], Sequence):
            return record.arguments[1]
        
class _fcntl:
    fd = mk_getfds(0)
class _fcntl64:
    fd = mk_getfds(0)
class _fsync:
    fd = mk_getfds(0)
class _fdatasync:
    fd = mk_getfds(0)
class _fstat:
    fd = mk_getfds(0)
class _dup:
    @staticmethod
    def fd(record: SyscallRecord, action=None) -> Collection[int]:
        if record.retval == -1:
            return tuple()
        else:
            return (record.retval, record.arguments[0])
class _dup2:
    @staticmethod
    def fd(record: SyscallRecord, action=None) -> Collection[int]:
        if record.retval == -1:
            return tuple()
        else:
            return (record.retval, record.arguments[0])

class _open:
    fd = mk_getfds(-1)
    
    @staticmethod
    def pathname(record: SyscallRecord, action=None):
        if isinstance(record.arguments[0], bytes):
            return record.arguments[0]
        elif record.arguments[0] == 'NULL' or isinstance(record.arguments[1], int):
            return None
        else:
            raise ValueError('_open: invalid pathname. record:', str(record))
    
    @staticmethod
    def flags(record: SyscallRecord, action=None) -> str:
        def flatten(expr: Expr|int|str) -> str:
            if isinstance(expr, int):
                return oct(expr)
            elif isinstance(expr, str):
                return expr
            elif isinstance(expr, Expr):
                if len(expr) == 1:
                    return expr[0] + flatten(expr[1])
                elif len(expr) == 2:
                    return flatten(expr[1]) + expr[0] + flatten(expr[2])
            else:
                raise TypeError(expr)
            
        return flatten(record.arguments[1])

class _openat:
    @staticmethod
    def fd(record, action=None):
        fds = []
        if isinstance(record.arguments[0], int):
            fds.append(record.arguments[0])
        elif isinstance(record.arguments[0], int) and record.arguments[0] == 'AT_FDCWD':
            fds.append(-100)
        else:
            fds.append(None)
        fds.append(record.retval if record.retval >= 0 else None)
        
        return tuple(fds)
    @staticmethod
    def pathname(record: SyscallRecord, action=None):
        if isinstance(record.arguments[1], bytes):
            return record.arguments[1]
        elif record.arguments[1] == 'NULL' or isinstance(record.arguments[1], int):
            return None
        else:
            raise ValueError('_open: invalid pathname. record:', str(record))
        
    @staticmethod
    def flags(record: SyscallRecord, action=None) -> str|None:

        def flatten(expr: Expr|int|str) -> str:
            if isinstance(expr, int):
                return oct(expr)
            elif isinstance(expr, str):
                return expr
            elif isinstance(expr, Expr):
                if len(expr) == 2:
                    return expr[0] + flatten(expr[1])
                elif len(expr) == 3:
                    return flatten(expr[1]) + expr[0] + flatten(expr[2])
            else:
                raise TypeError(expr)
        
        return flatten(record.arguments[2])

class _lseek:
    fd = mk_getfds(0)
class _close:
    fd = mk_getfds(0)

"""
    尽管SocketActions不要求里面的操作是合逻辑的, 但epoll系列的函数不得不检查当前SockActions之前是不是有epoll_ctl EPOLL_CTL_ADD
"""
class _epoll_create1:
    fd = mk_getfds(-1)
class _epoll_ctl:
    fd = mk_getfds(2)
class _epoll_wait:
    @staticmethod
    def fd(record, *actions) -> Sequence[int]:
        
        epolled_fds = set()
        for action in actions:
            for epoll_record in action.records:
                if epoll_record.syscall in 'epoll_ctl':
                    op = epoll_record.arguments[1]
                    ctled_fd = epoll_record.arguments[2]
                    if 'EPOLL_CTL_ADD' == op:
                        if isinstance(ctled_fd, int) and \
                            epoll_record.arguments[0] == record.arguments[0]:
                            # 
                            # epoll_ctl(x, EPOLL_CTL_ADD, y)
                            # ...
                            # epoll_wait(x, ...)
                            # 
                            # we got y as a fd to add
                            epolled_fds.add(ctled_fd)  
                        else:
                            print(f'_epoll_wait EPOLL_CTL_ADD warning: invalid ctled_fd: {ctled_fd}', str(record))
                    elif 'EPOLL_CTL_DEL' == op:
                        if isinstance(ctled_fd, int) and \
                            epoll_record.arguments[0] == record.arguments[0]:
                            # 
                            # epoll_ctl(x, EPOLL_CTL_DEL, y)
                            # ...
                            # epoll_wait(x, ...)
                            # 
                            # we got y as a fd to delete
                            epolled_fds.add(ctled_fd)  
                        else:
                            print(f'_epoll_wait EPOLL_CTL_DEL warning: invalid ctled_fd: {ctled_fd}', str(record))
                    elif 'EPOLL_CTL_MOD' == op:
                        ### 不影响找fd
                        pass
                    else:
                        print(f'_epoll_wait warning: invalid op {op}')

        return tuple(epolled_fds)


syscalls = {
    'socket': _socket, 'bind': _bind, 'listen': _listen, 'accept': _accept,
    'connect': _connect, 'send': _send, 'recv': _recv, 'sendto': _sendto,
    'recvfrom': _recvfrom, 'sendmsg': _sendmsg, 'recvmsg': _recvmsg, 
    'sendmmsg': _sendmmsg, 'recvmmsg': _recvmmsg,
    'getsockopt': _getsockopt,
    'setsockopt': _setsockopt, 'getsockname': _getsockname, 'getpeername': _getpeername, 'ioctl': _ioctl,
    'poll': _poll, 'select': _select, '_newselect': _newselect, 'fcntl': _fcntl, 'fcntl64': _fcntl64,
    'epoll_create1': _epoll_create1, 'epoll_ctl': _epoll_ctl, 'epoll_wait': _epoll_wait,
    'read': _read, 'write': _write, 'readv': _readv, 'writev': _writev, 
    'open': _open, 'close': _close, 'lseek': _lseek, 'fstat': _fstat, 
    'fsync': _fsync, 'fdatasync': _fdatasync, 'dup': _dup, 'dup2': _dup2, 
    'fcntl': _fcntl, 'ioctl': _ioctl, 'openat': _openat
}

for handler in syscalls.values():
    setattr(handler, 'error_desc', error_desc)

filesyscalls = {
    'ioctl': _ioctl, 'fcntl': _fcntl, 'fcntl64': _fcntl64,
    'read': _read, 'write': _write, 'readv': _readv, 'writev': _writev, 
    'open': _open, 'close': _close, 'lseek': _lseek, 'fstat': _fstat, 
    'fsync': _fsync, 'fdatasync': _fdatasync, 'dup': _dup, 'dup2': _dup2, 
    'fcntl': _fcntl, 'ioctl': _ioctl, 'openat': _openat
}

socketsyscalls = {
    'socket': _socket, 'bind': _bind, 'listen': _listen, 'accept': _accept,
    'connect': _connect, 'send': _send, 'recv': _recv, 'sendto': _sendto,
    'recvfrom': _recvfrom, 'sendmsg': _sendmsg, 'recvmsg': _recvmsg, 'sendmmsg': _sendmmsg, 'recvmmsg': _recvmmsg,
    'getsockopt': _getsockopt,
    'setsockopt': _setsockopt, 'getsockname': _getsockname, 'getpeername': _getpeername, 'ioctl': _ioctl,
    'poll': _poll, 'select': _select, '_newselect': _newselect, 'fcntl': _fcntl, 'fcntl64': _fcntl64,
    'epoll_create1': _epoll_create1, 'epoll_ctl': _epoll_ctl, 'epoll_wait': _epoll_wait,
    'read': _read, 'write': _write, 'readv': _readv, 'writev': _writev, 
    'close': _close, 'dup': _dup, 'dup2': _dup2,  'fcntl': _fcntl, 'ioctl': _ioctl,
}


@dataclass
class FileOperation:
    OPEN = filesyscalls['open']
    READ = filesyscalls['read']
    READV = filesyscalls['readv']
    WRITE = filesyscalls['write']
    WRITEV = filesyscalls['writev']
    CLOSE = filesyscalls['close']
    LSEEK = filesyscalls['lseek']
    FSTAT = filesyscalls['fstat']
    FSYNC = filesyscalls['fsync']
    FDATASYNC = filesyscalls['fdatasync']
    DUP = filesyscalls['dup']
    DUP2 = filesyscalls['dup2']
    FCNTL = filesyscalls['fcntl']
    IOCTL = filesyscalls['ioctl']
    OPENAT = filesyscalls['openat']

@dataclass
class SocketOperation:
    SOCKET = socketsyscalls['socket']
    BIND = socketsyscalls['bind']
    LISTEN = socketsyscalls['listen']
    ACCEPT = socketsyscalls['accept']
    CONNECT = socketsyscalls['connect']
    SEND = socketsyscalls['send']
    RECV = socketsyscalls['recv']
    SENDTO = socketsyscalls['sendto']
    RECVFROM = socketsyscalls['recvfrom']
    SENDMSG = socketsyscalls['sendmsg']
    RECVMSG = socketsyscalls['recvmsg']
    GETSOCKOPT = socketsyscalls['getsockopt']
    SETSOCKOPT = socketsyscalls['setsockopt']
    GETSOCKNAME = socketsyscalls['getsockname']
    GETPEERNAME = socketsyscalls['getpeername']
    IOCTL = socketsyscalls['ioctl']
    POLL = socketsyscalls['poll']
    SELECT = socketsyscalls['select']
    NEWSELECT = socketsyscalls['_newselect']
    FCNTL = socketsyscalls['fcntl']
    FCNTL64 = socketsyscalls['fcntl64']
    EPOLL_CREATE1 = socketsyscalls['epoll_create1']
    EPOLL_CTL = socketsyscalls['epoll_ctl']
    EPOLL_WAIT = socketsyscalls['epoll_wait']
    READ = socketsyscalls['read']
    WRITE = socketsyscalls['write']
    READV = socketsyscalls['readv']
    WRITEV = socketsyscalls['writev']
    CLOSE = socketsyscalls['close']
    DUP = socketsyscalls['dup']
    DUP2 = socketsyscalls['dup2']
    FCNTL = socketsyscalls['fcntl']
    IOCTL = socketsyscalls['ioctl']
    SENDMMSG = socketsyscalls['sendmmsg']
    RECVMMSG = socketsyscalls['recvmmsg']