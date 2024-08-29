from typing import Sequence

from ...record import SyscallRecord

def mk_getfd(_argpos=0):
    """
        >= 0: arguments[0] 
        -1  : retval
    """
    def getfd(record, action=None, argpos=_argpos):
        if argpos >= 0:
            return record.arguments[0]
        elif argpos == -1:
            return record.retval
    return getfd

def selectfds(record, _argpos=0):
    fds = tuple()
    if isinstance(record.arguments[_argpos], Sequence) and \
        not isinstance(record.arguments[_argpos], str):
        fds += tuple([pollfd for pollfd in record.arguments[_argpos]])
    elif record.arguments[_argpos] == 'NULL':
        fds += tuple()
    else:
        raise ValueError('_select: invalid arg1. '+str(record.arguments[_argpos]))
    return fds

class _socket:
    fd = mk_getfd(-1)
class _bind:
    fd = mk_getfd(0)
class _listen:
    fd = mk_getfd(0)
class _accept:
    @staticmethod
    def fd(record:SyscallRecord, action=None):
        fds = {record.arguments[0]}
        if isinstance(record.retval, int) and record.retval >= 0:
            fds.add(record.retval)
        return tuple(fds)
class _connect:
    fd = mk_getfd(0)
class _send:
    fd = mk_getfd(0)
class _recv:
    fd = mk_getfd(0)
class _sendto:
    fd = mk_getfd(0)
class _recvfrom:
    fd = mk_getfd(0)
class _sendmsg:
    fd = mk_getfd(0)
class _recvmsg:
    fd = mk_getfd(0)
class _getsockopt:
    fd = mk_getfd(0)
class _setsockopt:
    fd = mk_getfd(0)
class _getsockname:
    fd = mk_getfd(0)
class _getpeername:
    fd = mk_getfd(0)
class _ioctl:
    fd = mk_getfd(0)
class _poll:
    @staticmethod
    def fd(record: SyscallRecord, action=None) -> Sequence[int]:
        try:
            if isinstance(record.arguments[0], Sequence):
                return tuple([pollfd[0] for pollfd in record.arguments[0]])
            elif record.arguments[0] == 'NULL':
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
    fd = mk_getfd(0)
class _write:
    fd = mk_getfd(0)
class _readv:
    fd = mk_getfd(0)
class _writev:
    fd = mk_getfd(0)
class _fcntl:
    fd = mk_getfd(0)
class _fcntl64:
    fd = mk_getfd(0)

"""
    尽管SocketActions不要求里面的操作是合逻辑的, 但epoll系列的函数不得不检查当前SockActions之前是不是有epoll_ctl EPOLL_CTL_ADD
"""
class _epoll_create1:
    fd = mk_getfd(-1)
class _epoll_ctl:
    fd = mk_getfd(2)
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


class _dup:
    @staticmethod
    def fd(record: SyscallRecord, action=None):
        return (record.arguments[0], record.retval) if record.retval

sockmap = {
    'socket': _socket, 'bind': _bind, 'listen': _listen, 'accept': _accept,
    'connect': _connect, 'send': _send, 'recv': _recv, 'sendto': _sendto,
    'recvfrom': _recvfrom, 'sendmsg': _sendmsg, 'recvmsg': _recvmsg, 'getsockopt': _getsockopt,
    'setsockopt': _setsockopt, 'getsockname': _getsockname, 'getpeername': _getpeername, 'ioctl': _ioctl,
    'poll': _poll, 'select': _select, '_newselect': _newselect, 'fcntl': _fcntl, 'fcntl64': _fcntl64,
    'epoll_create1': _epoll_create1, 'epoll_ctl': _epoll_ctl, 'epoll_wait': _epoll_wait,
    'read': _read, 'write': _write, 'readv': _readv, 'writev': _writev, ''
}