from typing import TypeVar
from collections.abc import Iterable

from ..record import \
    SignalRecord, SyscallRecordNoArg, SignalParsingFailException, \
    SyscallRecord, SyscallParsingFailGeneralException, ResumingUnfinishedException, \
    UnexceptedRecord, UnexpectedParsingFailException

from ..record.prop import Property, PROPERTIES_GENERAL

class MultiLineError(Exception):
    """
        字符串中包含换行
    """

    def __init__(self, line: str, *args: object) -> None:
        super().__init__(*args)
        self.line = line

def parse(line: str) -> SignalRecord | SyscallRecord | UnexceptedRecord | None:
    """
        解析一个strace line, 成功返回对应的Record, 失败返回None
        除非代码错误, 否则不会抛出MultiLineError之外的异常. 
    """

    if line.find('\n') >= 0:
        raise MultiLineError(line)

    try:
        return SignalRecord(line)
    except SignalParsingFailException:
        pass
    try:
        return SyscallRecord(line)
    except SyscallParsingFailGeneralException:
        pass
    try:
        return UnexceptedRecord(line)
    except UnexpectedParsingFailException:
        pass

    return None


# 实验性代码, 但一般不影响可用性
RecordType = TypeVar('RecordType')
def parse_as(line: str, _t: RecordType) -> RecordType | None:
    """
        按照某个指定的Record类型解析

        line: 
        _t: 指定的解析类型, 例如SyscallRecord
    """

    try:
        return _t(line)
    except parse_as.ExceptionMap[_t] as e:
        return None
    
setattr(
    parse_as, 
    'ExceptionMap', 
    {
        SignalRecord: (SignalParsingFailException),
        SyscallRecord: (SyscallParsingFailGeneralException, ResumingUnfinishedException),
        SyscallRecordNoArg: (SyscallParsingFailGeneralException, ResumingUnfinishedException),
        UnexceptedRecord: (UnexpectedParsingFailException)
    }
)


Syscall = TypeVar('Syscall', SyscallRecord, SyscallRecordNoArg)
def match_syscalls(syscall_records: Iterable[Syscall]) -> tuple[list[Syscall], list[Syscall], list[Syscall]]:
    """
        排好序的一组SyscallRecord/SyscallRecordNoArg中, 
        生成合并后的一组对应的内容. 
        **不保证合并后的相对位置与合并前一致**
        TODO: 修改算法调整生成的合并后record的位置.

        syscall_records: 待匹配的一组SyscallRecord/SyscallRecordNoArg, 已经排好序. 

        return: 完成匹配的组, 匹配不到恢复的未完成组(unfinished), 匹配不到未完成的恢复组(resumed)
    """

    syscall_records = list(syscall_records)
    completed = []
    unfinished = []
    resuming = []
    while syscall_records:
        sr: SyscallRecord = syscall_records.pop(0)
        # print([str(i)+' '+str(_) for i, _ in list(reversed(list(enumerate(unfinished))))])
        if sr.complete:
            completed.append(sr)
        elif sr.unfinished:
            unfinished.append(sr)
        elif sr.resuming:
            # print('->', str(sr))
            i_unf, _the_merged = None, None
            for i, sr_unfinished in reversed(list(enumerate(unfinished))):
                if sr_unfinished.syscall == sr.syscall:
                    _the_merged = sr.merge(sr_unfinished)
                    if _the_merged is not None:
                        i_unf = i
                        break

            if isinstance(i_unf, int) and i_unf>=0 and _the_merged :
                completed.append(_the_merged)
                unfinished.pop(i_unf)
            else:
                resuming.append(sr)
                        

    return completed, unfinished, resuming

def parse_and_match_syscalls(lines: Iterable[str], _no_args=False) -> tuple[list[Syscall], list[Syscall], list[Syscall]]:
    """
        给定一组按照时间排好序的strace line, 尽可能地解析所
        有的系统调用信息, 并将不完整的部分匹配并合并. 关于匹配
        与合并, 见match_syscalls

        lines:
        _no_args: 是否解析系统调用参数, False时生成SyscallRecordNoArg, True时生成SyscallRecord

        return: 完成匹配的组, 匹配不到恢复的未完成组(unfinished), 匹配不到未完成的恢复组(resumed)
    """

    if _no_args:
        syscall_records = [parse_as(line, SyscallRecordNoArg) for line in lines]
        syscall_records = [_ for _ in syscall_records if _]
    else:
        syscall_records = [parse_as(line, SyscallRecord) for line in lines]
        syscall_records = [_ for _ in syscall_records if _]

    return match_syscalls(syscall_records)

def parse_auto(lines: Iterable[str], _match_syscall=False) -> tuple[list[SyscallRecord], list[SignalRecord], list[UnexceptedRecord], list[str]]:
    
    """
        尝试解析所有已知的strace line: SyscallRecord, SignalRecord, SyscallRecordNoArg, UnexceptedRecord

        _match_syscall: True会在解析结束之后尝试将所有系统调用信息中的unfinished与resumed匹配起来, 需要lines是排好序的. (见match_syscalls)

        return: SyscallRecord组, SignalRecord组, UnexceptedRecord组, 失败的匹配
    """
    syscall_records = []
    signal_records = []
    unexpected_records = []
    failed_lines = []

    for line in lines:
        
        # 大部分时间里, 处理的都是syscall, 所以先尝试它
        # 解析参数很费时间, 所以不解析参数来判断是不是系统调用
        if parse_as(line, SyscallRecordNoArg) is not None:
            sr = parse_as(line, SyscallRecord)
            if sr is not None: 
                syscall_records.append(sr)
                continue
        
        sigr = parse_as(line, SignalRecord)
        if sigr:
            signal_records.append(sigr)
            continue

        unxr = parse_as(line, UnexceptedRecord)
        if unxr:
            unexpected_records.append(unxr)
            continue

        failed_lines.append(line)
        continue
    
    if _match_syscall:

        unfinished, resuming = 0, 0
        for sr in syscall_records:
            if sr.unfinished:
                unfinished += 1
            elif sr.resuming:
                resuming += 1

        c, u, r = match_syscalls(syscall_records)
        syscall_records = c + u + r

    return syscall_records, signal_records, unexpected_records, failed_lines
        
def parse(lines: Iterable[str], _syscall_prop: dict=None, _signal_prop:dict=None, _unexpected_prop:dict=None) \
        -> tuple[list[SyscallRecord], list[SignalRecord], list[UnexceptedRecord], list[str]]:

    syscall_records, signal_records, unexpected_records, failed_lines = parse_auto(lines, True)
    
    if _syscall_prop is None:
        _syscall_prop = PROPERTIES_GENERAL
    if _signal_prop is None:
        _signal_prop = {}
    if _unexpected_prop is None:
        _unexpected_prop = {}

    _SyscallType = type('Syscall', (SyscallRecord, Property(_syscall_prop)), {})
    _SignalType = type('Signal', (SignalRecord, Property(_signal_prop)), {})
    _UnexpectedType = type('Unexpected', (UnexceptedRecord, Property(_unexpected_prop)), {})
    return \
        [_SyscallType(_.origin_line) for _ in syscall_records if (_.retval is not None and _.arguments is not None)], \
        [_SignalType(_.origin_line) for _ in signal_records], \
        [_UnexpectedType(_.origin_line) for _ in unexpected_records], \
        failed_lines