from typing import Iterable, Sequence
from time import time
import multiprocessing
from multiprocessing import Process, Queue, Pool, Lock

from .parse import parse_as, match_syscalls
from ..record import SyscallRecord, SyscallRecordNoArg

def parsetask(lines: Sequence[str], index: int) -> tuple[Sequence[SyscallRecord], Sequence[str], int]:
    syscalls, fails = [], []
    for line in lines:
        record = parse_as(line, SyscallRecord)
        if record is None:
            fails.append(line)
        else:
            syscalls.append(record)
    return syscalls, fails, index

def parse_multiprocess(
            lines: Sequence[str], 
            batchsize: int=10**5,
            batchcount: int=-1,
            syscall_only=True
        ):
    
    
    BATCHSIZE = batchsize
    BATCHCOUNT = batchcount
    if not syscall_only:
        raise NotImplementedError
    
    syscalldict, faileddict = {}, {}
    syscalls, faileds = [], []
    asyncresults = []
    timestamp = time()
    with Pool(processes=20) as pool:
        
        ### build tasks && put to pool
        _batchs = 0
        while len(lines):
            asyncresults.append(
                pool.apply_async(parsetask, (lines[:BATCHSIZE], _batchs))
            )
            lines = lines[BATCHSIZE:]
            _batchs += 1
            if BATCHCOUNT > 0 and _batchs >= BATCHCOUNT:
                break

        pool.close()
        pool.join()


        for res in asyncresults:
            _syscalls, _faileds, index = res.get(timeout=1)
            syscalldict[index] = _syscalls
            faileddict[index] = _faileds

        for i in range(len(syscalldict)):
            syscalls += syscalldict[i]
        for i in range(len(faileddict)):
            faileds += faileddict[i]

    total = len(syscalls)+len(faileds) if len(syscalls)+len(faileds) > 0 else 1
    print(f'\t({len(syscalls)+len(faileds)}) parsed in {time()-timestamp}s')
    print(f'\t\tsuccess {100*len(syscalls)/(total):.4f}%')
    print(f'\t\tfailed {100*len(faileds)/(total):.4f}%')

    print('\tstart matching')
    timestamp = time()
    matchsucc, unfinished, resumed = match_syscalls(syscalls)
    print(f'\tmatch finished in {time()-timestamp}')
    _sum = len(matchsucc) + len(unfinished) + len(resumed) if \
                len(matchsucc) + len(unfinished) + len(resumed) != 0 else 1
    print(f'\t\tsuccess {100*len(matchsucc)/_sum:.4f}% ({len(matchsucc)})')
    print(f'\t\tunfinished {100*len(unfinished)/_sum:.4f}% ({len(unfinished)})')
    print(f'\t\tresumed {100*len(resumed)/_sum:.4f}% ({len(resumed)})')

    return syscalls, faileds

    