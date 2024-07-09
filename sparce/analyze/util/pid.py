from typing import Sequence

from ...record import SyscallRecord

def classify_by_pid(records: Sequence[SyscallRecord]) -> dict[int, tuple[SyscallRecord]]:
    classified = {}
    for record in records:
        if record.pid not in classified:
            classified[record.pid] = []
        classified[record.pid].append(record)
    for pid in classified:
        classified[pid] = tuple(classified[pid])
    return classified
