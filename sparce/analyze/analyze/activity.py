from typing import Sequence
from copy import copy, deepcopy

from ...record import SyscallRecord
from ...record import types as parsed_t

class _open:
    NAME = 'open'
    @staticmethod
    def keyword(record: SyscallRecord) -> str:
        return record.arguments[0].value.decode('utf-8')
    @staticmethod
    def newfd(record: SyscallRecord) -> int:
        return record.retval
    fd = newfd

class _socket:
    NAME = 'socket'
    @staticmethod
    def newfd(record: SyscallRecord) -> int:
        return record.retval

class _accept:
    NAME = 'accept'
    @staticmethod
    def newfd(record: SyscallRecord) -> int:
        return record.retval
    @staticmethod
    def oldfd(record: SyscallRecord) -> int:
        return record.arguments[0].value

class _bind:
    NAME = 'bind'
    @staticmethod
    def keyword(record: SyscallRecord) -> str:
        return str(record.arguments[1].value)

class _getsockname:
    NAME = 'getsockname'
    @staticmethod
    def keyword(record: SyscallRecord) -> str:
        return str(record.arguments[1].value)
    
    @staticmethod
    def fd(record: SyscallRecord) -> int:
        return record.arguments[0].value

class _dup:
    NAME = 'dup'
    @staticmethod
    def newfd(record: SyscallRecord) -> int:
        return record.retval
    @staticmethod
    def oldfd(record: SyscallRecord) -> int:
        return record.arguments[0].value
    
class _dup2:
    NAME = 'dup2'
    @staticmethod
    def newfd(record: SyscallRecord) -> int:
        return record.retval
    @staticmethod
    def oldfd(record: SyscallRecord) -> int:
        return record.arguments[0].value

class _close:
    NAME = 'close'
    @staticmethod
    def fd(record: SyscallRecord) -> int:
        return record.arguments[0].value

class Activity(list):
    
    def __init__(self, *args, **kwargs):
        
        self.keyword = kwargs.pop('keyword', None)
        
        super().__init__(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self[0].timestamp}->{self[-1].timestamp}' + (self.keyword if self.keyword else '') + ' '.join((_.syscall for _ in self))
    

def activities(syscall_records: Sequence[SyscallRecord]) -> Sequence[Activity]:
    
    APPLYING = (_open, _socket)
    GENFROM = (_accept, _dup, _dup2)
    KEYWORDing = (_open, _getsockname, _bind)
    RELEASING = (_close, )

    def _is_applying(record: SyscallRecord) -> bool:
        return record.syscall in (_.NAME for _ in APPLYING)
    
    def _new_activity(record: SyscallRecord) -> tuple[Activity, int]:
        for _ in APPLYING:
            if record.syscall == _.NAME:
                return Activity((record, )), _.newfd(record) 
    
    def _get_using_fd(record: SyscallRecord, identifiers) -> int | None:
        if record.arguments is None:
            return None
        _ =  tuple(set(identifiers) & {_.value for _ in record.arguments if isinstance(_.value, int)})
        return _[0] if len(_) == 1 else None

    def _is_keywording(record: SyscallRecord) -> bool:
        return record.syscall in (_.NAME for _ in KEYWORDing)
    
    def _get_keywording_fd(record: SyscallRecord) -> int:
        for _ in KEYWORDing:
            if record.syscall == _.NAME:
                return _.fd(record)
        raise ValueError(f'{record.syscall} not keywording')
    
    def _get_keyword(record: SyscallRecord) -> str:
        for _ in KEYWORDing:
            if record.syscall == _.NAME:
                return _.keyword(record)
        raise ValueError(f'{record.syscall} not keywording')
    
    def _is_releasing(record: SyscallRecord) -> bool:
        return record.syscall in (_.NAME for _ in RELEASING)
    
    def _get_releasing(record: SyscallRecord) -> int:
        for _ in RELEASING:
            if record.syscall == _.NAME:
                return _.fd(record)
        raise ValueError(f'{record.syscall} not releasing')
    
    def _is_genfrom(record: SyscallRecord) -> bool:
        return record.syscall in (_.NAME for _ in GENFROM)
    
    def _get_genfrom(record: SyscallRecord) -> tuple[int, int]:
        for _ in GENFROM:
            if record.syscall == _.NAME:
                return _.oldfd(record), _.newfd(record)
        raise ValueError(f'{record.syscall} not genfrom')

    syscall_records = copy(syscall_records) # 不要破坏掉原来的list对其元素的引用

    working = {}
    backward_records = []
    done = []
    # forward
    for record in syscall_records:    
        
        if _is_applying(record):
            newact, newfd = _new_activity(record)
            working[newfd] = newact
        
        elif _is_genfrom(record):
            oldfd, newfd = _get_genfrom(record)
            if oldfd in working.keys():
                newact = deepcopy(working[oldfd])
                newact.append(record)
                working[newfd] = newact
            else:
                backward_records.insert(0, record)
        
        elif _is_releasing(record):
            fd = _get_releasing(record)
            if fd in working.keys():
                working[fd].append(record)
                done.append(working.pop(fd))
            else:
                backward_records.insert(0, record)
        else:

            fd = _get_using_fd(record, working.keys())
            if fd is not None:
                working[fd].append(record)
            else:
                backward_records.insert(0, record)

        if _is_keywording(record):
            keyword = _get_keyword(record)
            fd = _get_keywording_fd(record)
            if fd is not None:
                working[fd].keyword = keyword
    
    done += list(working.values())


    # backward
    # 补一个反向搜索用来搜索"只有后一半"的activities, 可能有些fd在forward过程中没有对应的申请或生成过程
    
    backward_working = {}
    for record in backward_records:

        if _is_releasing(record):
            fd, newact = _get_releasing(record), Activity((record, ))
            backward_working[fd] = newact
        elif _is_genfrom(record):
            oldfd, newfd = _get_genfrom(record)
            if newfd in backward_working.keys():
                backward_working[newfd].append(record)
                newact = deepcopy(backward_working[newfd])
                backward_working[oldfd] = newact
        else:
            fd = _get_using_fd(record, backward_working.keys())
            if fd is not None:
                backward_working[fd].append(record)

        if _is_keywording(record):
            keyword = _get_keyword(record)
            fd = _get_keywording_fd(record)
            if fd is not None:
                backward_working[fd].keyword = keyword
    
    
    done += list(backward_working.values())
    
    return tuple(done)
            