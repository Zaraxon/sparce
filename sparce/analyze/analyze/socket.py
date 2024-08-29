from typing import Sequence
from collections.abc import Container

from ...record import SyscallRecord

from .socket__ import sockmap

class SocketActivity:
    """
        SyscallRecord 的容器类. 将一组SyscallRecords置于上下文中以获取更多有效信息.
        同一个SocketActions中的SyscallRecords操作同一个生命周期的fd. 即, close后再申请是另一个生命周期. 

        只要求SocketActions是按时间顺序的

        不要求SocketActions的操作是合逻辑的
    """
    def __init__(
            self, 
            records: Sequence[SyscallRecord],
            fd: int
            ):
        self.records = tuple(records)
        self.fd = fd
    
    @property
    def addr(self):
        if not hasattr(self, '_addr'):
            addr = None
            for r in self.records:
                if r.syscall == 'bind' and getattr(r, 'arguments', None):
                    addr = r.arguments[1]
                    break
                elif r.syscall == 'connect' and getattr(r, 'arguments', None):
                    addr = r.arguments[1]
                    break
                elif r.syscall == 'getsockname' and getattr(r, 'arguments', None):
                    addr = r.arguments[1]
                    break
                elif r.syscall == 'accept' and (self.fd == r.retval) \
                    and getattr(r, 'arguments', None):
                    addr = r.arguments[1]
                    break
            self._addr = addr
        return self._addr

def sockactions(records: Sequence[SyscallRecord]) -> Sequence[SocketActivity]:
    
    sockaction_dict = dict()

    for r in records:
        
        handler = sockmap.get(r.syscall)
        if handler is None:
            continue

        if r.syscall == 'epoll_wait':
            fds = handler.fd(r, *sockaction_dict.values())
        else:
            fds = handler.fd(r)
        
        if isinstance(fds, int):
            fds = {fds}
        elif fds is None:
            fds = {}

        if not isinstance(fds, Container):
            print('fds:', fds, type(fds))
            print('record', str(r))
            assert False

        for fd in fds:
            if fd not in sockaction_dict.keys():
                sockaction_dict[fd] = SocketActivity([r], fd)
            sockaction_dict[fd].records += (r, )
        
    return tuple(sockaction_dict.values())