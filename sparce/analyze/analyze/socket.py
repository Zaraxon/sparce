from typing import Sequence, Mapping
from collections.abc import Collection, Iterable

from ...record import SyscallRecord
from ...record.types import Structure

from .info import socketsyscalls, SocketOperation



class SocketActivity:
    """
        SyscallRecord 的容器类. 将一组SyscallRecords置于上下文中以获取更多有效信息.
        同一个SocketActivity中的SyscallRecords操作同一个生命周期的fd. 即, close后再申请是另一个生命周期. 

        只要求SocketActivity是按时间顺序的, 不要求SocketActivity的操作是合逻辑的(考虑到tracee的行为本身难以预测).

        当SocketActivity导出信息时应当导出对应的"有效行为". 例如read的返回值为-1时, read内容不应该作为SockActivity读取行为的一部分.
    """

    @staticmethod
    def __bufdata(record: SyscallRecord) -> tuple[bytes, int]:

        #   对于一个SyscallRecord来说, count和buf有四种情况
        #   count = -1/>=0, buf=None/bytes
        #   count = -1/0时可以直接认为是读/写了一个b''
        #   count > 0, buf=bytes是正常情况
        #   count > 0, buf=None则是异常情况, 此时应该告知外部"有写count个字节, 但写了什么不知道"
        #   综合以上情况, count和buf应该共同返回, buf总应该是bytes来保证易用性

        handler = socketsyscalls[record.syscall]

        count = handler.count(record)
        buf = handler.buf(record)
        if count <= 0:
            return (b'', count)
        else:
            if isinstance(buf, bytes):
                return (buf[:count], count)
            else:
                # 意外情况, 可能发生在buf只有个0xabcd1234这样的地址时
                # 返回有效的count, 和b''来保证易用性
                return (b'', count)
            
    @staticmethod
    def __iovdata(record: SyscallRecord) -> tuple[bytes, int]:

        handler = socketsyscalls[record.syscall]

        count = handler.count(record)
        iov = handler.iov(record)
        if count <= 0:
            return (b'', count)
        else:
            if isinstance(iov, Sequence):
                data = b'' .join(_io[0] for _io in iov)[:count]
                return (data, count)
            else:
                return (b'', count)

    def __init__(
            self, 
            records: Sequence[SyscallRecord],
            fd: int
            ):
        self.__records = tuple(records)
        self.fd = fd

        # find address
        addr = None
        for r in self.__records:
            if r.syscall == 'bind' and isinstance(r.arguments[1], Structure):
                addr = r.arguments[1]
                break
            elif r.syscall == 'connect' and isinstance(r.arguments[1], Structure):
                addr = r.arguments[1]
                break
            elif r.syscall == 'getsockname' and isinstance(r.arguments[1], Structure):
                addr = r.arguments[1]
                break
            elif r.syscall == 'accept' and (self.fd == r.retval) and isinstance(r.arguments[1], Structure):
                addr = r.arguments[1]
                break
        self.__addr = addr

        # find data
        self.__dataflows_in, self.__dataflows_out = [], []
        for r in self.__records:
            if r.syscall in {'send', 'recv', 'sendto', 'recvfrom'}:
                data, count = self.__bufdata(r)
                if count > 0:
                    if r.syscall in {'recv', 'recvfrom'}:
                        self.__dataflows_in.append((data, count))
                    else:
                        self.__dataflows_out.append((data, count))
            # TODO: sendmsg/recvmsg/sendmmsg/recvmmsg这里被strace decode后难以被count检查, 这里暂时不管count只给出原始的Structure/tuple[Structure]
            elif r.syscall == 'sendmsg':
                count = SocketOperation.SENDMSG.count(r)
                msg = SocketOperation.SENDMSG.msg(r)
                if msg is not None and count >= 0:
                    self.__dataflows_out.append((msg, count))
            elif r.syscall == 'recvmsg':
                count = SocketOperation.RECVMSG.count(r)
                msg = SocketOperation.RECVMSG.msg(r)
                if msg is not None and count >= 0:
                    self.__dataflows_in.append((msg, count))
            elif r.syscall == 'sendmmsg':
                count = SocketOperation.SENDMMSG.count(r)
                msgvec = SocketOperation.SENDMMSG.msgvec(r)
                if msgvec is not None and count >= 0:
                    self.__dataflows_out.append((msg, count))
            elif r.syscall == 'recvmmsg':
                count = SocketOperation.RECVMMSG.count(r)
                msgvec = SocketOperation.RECVMMSG.msgvec(r)
                if msgvec is not None and count >= 0:
                    self.__dataflows_in.append((msg, count))
        self.__dataflows_in, self.__dataflows_out = \
            tuple(self.__dataflows_in), tuple(self.__dataflows_out)
        
        # datafaileds
        self.__datafaileds = []
        for r in self.__records:
            if r.syscall in {'read', 'readv', 'write', 'writev'} and r.retval == -1:
                self.__datafaileds.append(r)
        self.__datafaileds = tuple(self.__datafaileds)

        # role
        self.__role = None
        for r in self.__records:
            if r.syscall in {'accept', 'listen', 'bind'} and r.retval >= 0:
                self.__role = 'server'
                break
            elif r.syscall in {'connect'} and r.retval >= 0:
                self.__role = 'client'
                break
        
        # listen status
        self.__listenstatus = None
        if self.role == 'client':
             for r in self.__records:
                if r.syscall in {'connect'} and r.retval >= 0:
                    self.__listenstatus = 'established'
                    break
        elif self.role == 'server':
            for r in self.__records:
                if r.syscall == 'bind':
                    if r.retval == 0:
                        self.__listenstatus = 'bind'
                    else:
                        break
                elif r.syscall == 'listen' and self.__listenstatus == 'bind':
                    if r.retval == 0:
                        self.__listenstatus = 'listen'
                    else:
                        break
                elif r.syscall == 'accept' and self.__listenstatus == 'listen':
                    if r.retval >= 0:
                        self.__listenstatus = 'accept'
                        break
                    else:
                        break
            
    @property
    def addr(self):
        return self.__addr
    
    @property
    def reads(self) -> list[tuple[bytes, int]]:
        return self.__dataflows_in
    @property
    def writes(self) -> list[tuple[bytes, int]]:
        return self.__dataflows_out
    
    @property
    def datafaileds(self):
        return self.__datafaileds
    
    @property
    def role(self):
        return self.__role
    
    @property
    def listenstatus(self):
        return self.__listenstatus


import time
def sockactivities(records: Sequence[SyscallRecord]) -> Collection[SocketActivity]:
    
    sockaction_dict = dict()
    done = list()

    ts = time.time()
    count, stride = 0, (len(records)+(5-1)) // 5
    for r in records:
        
        count += 1
        if count % stride == 0 and len(records) >= 1*(10**4):
            print(f'\tsockactivities: {100*count/len(records):.4f}% ({count}) parsed in {time.time()-ts}s')
        
        handler = socketsyscalls.get(r.syscall)
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

        if not isinstance(fds, Collection):
            print('fds:', fds, type(fds))
            print('record', str(r))
            assert False

        for fd in fds:
            if fd not in sockaction_dict:
                sockaction_dict[fd] = list()
            sockaction_dict[fd].append(r)
            if r.syscall == 'close':
                done.append(SocketActivity(sockaction_dict.pop(fd), fd))

    return tuple(done) + \
            tuple(SocketActivity(recordlist, fd) for fd, recordlist in sockaction_dict.items())

def group_as_addr(activities: Collection[SocketActivity]) -> Collection[Collection[SocketActivity]]:
    
    addr_dict = {}
    for act in activities:
        if act.addr is None:
            continue
        key = hash(act.addr)
        if key not in addr_dict.keys():
            addr_dict[key] = set()
        addr_dict[key].add(act)

    return tuple(addr_dict.values())

def group_as_addr_binary(activities: Iterable[SocketActivity]) -> Mapping[str, str]:
    """
        要求每个activity都有binary字段, 设置为对应的binary的名字
    """
    actdict = {}
    for act in activities:
        if act.addr is None:
            continue
        
        key = act.addr
        if key not in actdict.keys():
            actdict[key] = set()
        actdict[key].add(act.binary)
    
    return actdict
