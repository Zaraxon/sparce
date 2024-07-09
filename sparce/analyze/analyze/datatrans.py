from typing import Generator

from ...record import SyscallRecord
from ...record.types import Structure

from .activity import Activity, activities

class _read:
    NAME = 'read'
    @staticmethod
    def data(record: SyscallRecord) -> bytes | None:
        return record.arguments[1].value if isinstance(record.arguments[1].value, bytes) else None

class _send:
    NAME = 'send'
    @staticmethod
    def data(record: SyscallRecord) -> bytes | None:
        return record.arguments[1].value if isinstance(record.arguments[1].value, bytes) else None

class _readv:
    NAME = 'readv'
    @staticmethod
    def data(record: SyscallRecord) -> bytes | None:
        data = b''.join(
            (item.value['iov_base'] for item in record.arguments[1].value)
        )
        return data if data else None

class _write:
    NAME = 'write'
    @staticmethod
    def data(record: SyscallRecord) -> bytes | None:
        return record.arguments[1].value if isinstance(record.arguments[1].value, bytes) else None

class _recv:
    NAME = 'recv'
    @staticmethod
    def data(record: SyscallRecord) -> bytes | None:
        return record.arguments[1].value if isinstance(record.arguments[1].value, bytes) else None
    
class _writev:
    NAME = 'writev'
    @staticmethod
    def data(record: SyscallRecord) -> bytes | None:
        data = b''.join(
            (item.value['iov_base'] for item in record.arguments[1].value)
        )
        return data if data else None

INPUTING = [ _read, _recv, _readv ]
OUTPUTING = [ _write, _send , _writev ]

def data_in(activity: Activity) -> list[bytes]:
    """
        获取activity中"流入"的所有数据
        
        注: 任何意外情况下不会报错
    """
    
    def _is_input(record: SyscallRecord) -> bool:
        return record.syscall in [cls.NAME for cls in INPUTING]
    
    def _get_input_data(record: SyscallRecord) -> bytes:
        for _ in INPUTING:
            if record.syscall == _.NAME:
                data = _.data(record)
                break
        return data if data else b''
    
    all_data_in = []
    for record in activity:
        if _is_input(record):
            curr_data_in = _get_input_data(record)
            if curr_data_in:
                all_data_in.append(curr_data_in)

    return all_data_in



def data_out(activity: Activity) -> list[bytes]:
    
    """
        获取activity中"流出"的所有数据
        
        注: 任何意外情况下不会报错
    """

    def _is_output(record: SyscallRecord) -> bool:
        return record.syscall in [cls.NAME for cls in OUTPUTING]

    def _get_output_data(record: SyscallRecord) -> bytes:
        for _ in OUTPUTING:
            if record.syscall == _.NAME:
                data = _.data(record)
                break
        return data if data else b''
    
    all_data_out = []
    for record in activity:
        if _is_output(record):
            curr_data_out = _get_output_data(record)
            if curr_data_out:
                all_data_out.append(curr_data_out)

    return all_data_out
