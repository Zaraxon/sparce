from typing import Sequence
from ...record import SyscallRecord
from ...record import types as parsed_t

class _open:
    NAME = 'open'
    @staticmethod
    def keyword(record: SyscallRecord) -> str:
        return record.arguments[0].value.decode('utf-8')
    @staticmethod
    def identifier(record: SyscallRecord) -> int:
        return record.retval

class _socket:
    NAME = 'socket'
    @staticmethod
    def identifier(record: SyscallRecord) -> int:
        return record.retval

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

class _dup:
    NAME = 'dup'
    @staticmethod
    def identifier(record: SyscallRecord) -> int:
        return record.retval
    
class _dup2:
    NAME = 'dup2'
    @staticmethod
    def identifier(record: SyscallRecord) -> int:
        return record.retval

class _close:
    NAME = 'close'
    @staticmethod
    def identifier(record: SyscallRecord) -> int:
        return record.arguments[0].value

class Activity(list):
    
    def __init__(self, *args, **kwargs):
        
        keyword, identifier = kwargs.pop('keyword', None), kwargs.pop('identifier', None)
        if identifier is None:
            raise ValueError('Activity needs an identifier')
        
        self.keyword, self.identifier = keyword, identifier

        super().__init__(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self[0].timestamp}->{self[-1].timestamp}' + (self.keyword if self.keyword else '') + ' '.join((_.syscall for _ in self))
    

def activities(syscall_records: Sequence[SyscallRecord]) -> Sequence[Activity]:
    
    APPLYING = [_open, _socket, _dup, _dup2]
    KEYWORDing = [_open, _getsockname, _bind]
    RELEASING = [_close, ]

    def _is_applying(record: SyscallRecord) -> bool:
        return record.syscall in (_.NAME for _ in APPLYING)
    
    def _new_activity(record: SyscallRecord) -> Activity:
        for _ in APPLYING:
            if record.syscall == _.NAME:
                return Activity(
                    (record, ), 
                    identifier = _.identifier(record)
                )
        raise ValueError(f'{record.syscall} not applying')
    
    def _get_using_identifier(record: SyscallRecord, identifiers) -> int | None:
        _ =  tuple(set(identifiers) & {_.value for _ in record.arguments if isinstance(_.value, int)})
        return _[0] if len(_) == 1 else None

    def _is_keywording(record: SyscallRecord) -> bool:
        return record.syscall in (_.NAME for _ in KEYWORDing)
    
    def _get_keyword(record: SyscallRecord) -> str:
        for _ in KEYWORDing:
            if record.syscall == _.NAME:
                return _.keyword(record)
        raise ValueError(f'{record.syscall} not keywording')
    
    def _is_releasing(record: SyscallRecord) -> bool:
        return record.syscall in (_.NAME for _ in RELEASING)
    
    working = {}
    done = []
    for record in syscall_records:    
        
        if _is_applying(record):
            new = _new_activity(record)
            working[new.identifier] = new
            print('applying: ', new)

        if _is_keywording(record):
            keyword = _get_keyword(record)
            _id = _get_using_identifier(record, working.keys())
            if _id is not None:
                working[_id].keyword = keyword
            else:
                pass
                # print(f'warning: keyword {keyword} matched no identifier')
        
        if _is_releasing(record):
            _id = _get_using_identifier(record, working.keys())
            if _id is not None:
                working[_id].append(record)
                done.append(working.pop(_id))
            else:
                pass
                # print(f'warning: releasing id {_id} matched no identifier', record)
        
        if not _is_applying(record) and not _is_releasing(record):
            _id = _get_using_identifier(record, working.keys())
            if _id is not None:
                print(f'appending: {working[_id]}', record)
                working[_id].append(record)
                
    
    return tuple(done)
            