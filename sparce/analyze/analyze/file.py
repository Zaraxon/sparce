from typing import Sequence, Iterable
from collections.abc import Collection, Mapping

from ...record.types import Structure
from ...record import SyscallRecord

from .info import FileOperation, filesyscalls

class FileActivity:
    """
        SyscallRecord 的容器类. 将一组SyscallRecords置于上下文中以获取更多有效信息.
        同一个FileActivity中的SyscallRecords操作同一个生命周期的fd. 即, close后再申请是另一个生命周期. 

        只要求FileActivity是按时间顺序的

        不要求FileActivity的操作是合逻辑的
    """
    @staticmethod
    def _bufdata(record: SyscallRecord) -> tuple[bytes, int]:

        #   对于一个SyscallRecord来说, count和buf有四种情况
        #   count = -1/>=0, buf=None/bytes
        #   count = -1/0时可以直接认为是读/写了一个b''
        #   count > 0, buf=bytes是正常情况
        #   count > 0, buf=None则是异常情况, 此时应该告知外部"有写count个字节, 但写了什么不知道"
        #   综合以上情况, count和buf应该共同返回, buf总应该是bytes来保证易用性

        handler = filesyscalls[record.syscall]

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
    def _iovdata(record: SyscallRecord) -> tuple[bytes, int]:

        handler = filesyscalls[record.syscall]

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

        # find pathname
        _pathname = None
        for r in self.__records:
            if r.syscall == 'open':
                _pathname = FileOperation.OPEN.pathname(r)
                break
            elif r.syscall == 'openat':
                _pathname = FileOperation.OPENAT.pathname(r)
                break    
        self.__pathname = _pathname

        # read & write
        self.__dataflows_in, self.__dataflows_out = [], []
        for r in self.__records:
            if r.syscall in {'read', 'write'}:
                data, count = self._bufdata(r)
                if count > 0:
                    if r.syscall in {'read'}:
                        self.__dataflows_in.append((data, count))
                    else:
                        self.__dataflows_out.append((data, count))
            elif r.syscall in {'readv', 'writev'}:
                data, count = self._iovdata(r)
                if count > 0:
                    if r.syscall in {'readv'}:
                        self.__dataflows_in.append((data, count))
                    else:
                        self.__dataflows_out.append((data, count))
                        
        self.__dataflows_in, self.__dataflows_out = \
            tuple(self.__dataflows_in), tuple(self.__dataflows_out)
        
        # flags
        self.__flags = None
        for r in self.__records:
            if r.syscall == 'open' and r.retval >= 0:
                flags = FileOperation.OPEN.flags(r)
                if flags is not None:
                    self.__flags = flags
                    break
            elif r.syscall == 'openat':
                flags = FileOperation.OPENAT.flags(r)
                if flags is not None and r.retval >= 0:
                    self.__flags = flags
                    break
        
        # datafaileds
        self.__datafaileds = []
        for r in self.__records:
            if r.syscall in {'read', 'readv', 'write', 'writev'} and r.retval == -1:
                self.__datafaileds.append(r)
        self.__datafaileds = tuple(self.__datafaileds)
    
    @property
    def records(self):
        return tuple(self.__records)    

    @property
    def pathname(self):            
        return self.__pathname
    
    @property
    def reads(self):
        return self.__dataflows_in
    
    @property
    def writes(self):
        return self.__dataflows_out

    @property
    def datafaileds(self):
        return self.__datafaileds
    
    @property
    def flags(self):
        return self.__flags
    
    @property
    def open_first(self):
        for r in self.__records:
            if r.syscall == 'open':
                return r
            elif r.syscall == 'openat':
                return r
        return None
    

import time
def fileactivities(records: Sequence[SyscallRecord]) -> Collection[FileActivity]:
    
    fileaction_dict = dict()
    done = list()

    ts = time.time()
    count, stride = 0, (len(records)+(5-1)) // 5
    for r in records:
        
        count += 1
        if count % stride == 0 and len(records) >= 1*(10**4):
            print(f'\tfileactivities: {100*count/len(records):.4f}% ({count}) parsed in {time.time()-ts}s')
        
        handler = filesyscalls.get(r.syscall)
        if handler is None:
            continue

        if r.syscall == 'epoll_wait':
            fds = handler.fd(r, *fileaction_dict.values())
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
            if fd not in fileaction_dict:
                fileaction_dict[fd] = list()
            fileaction_dict[fd].append(r)
            if r.syscall == 'close':
                done.append(FileActivity(fileaction_dict.pop(fd), fd))

    return tuple(done) + \
            tuple(FileActivity(recordlist, fd) for fd, recordlist in fileaction_dict.items())

def group_as_pathname(activities: Collection[FileActivity]) -> Collection[Collection[FileActivity]]:
    
    pathname_dict = {}
    for act in activities:
        if act.pathname is None:
            continue
        key = hash(act.pathname)
        if key not in pathname_dict.keys():
            pathname_dict[key] = set()
        pathname_dict[key].add(act)
        
    return tuple(pathname_dict.values())

def group_as_binarypath(activities: Collection) -> Collection[Collection]:
    binaryname_dict = {}
    for act in activities:
        if act.binary is None:
            continue
        key = hash(act.binarypath)
        if key not in binaryname_dict.keys():
            binaryname_dict[key] = set()
        binaryname_dict[key].add(act)
        
    return tuple(binaryname_dict.values())