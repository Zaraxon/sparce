from typing import Sequence

from ...record import SyscallRecord

def build_absolute_timestamp(records: Sequence[SyscallRecord], start: float=0.000001) -> None:
    
    records[0].timestamp = start
    for i in range(1, len(records)):
        records[i].timestamp += records[i-1].timestamp