
## Overview

这是一个用来将strace生成的log文件处理为结构化数据的小工具库. 

## Quick Start

以下内容取自Ubuntu 22.04.1虚拟机中, 对命令`tar -czvf ln.zip /usr/bin/ln`的strace记录. 

> 这些strace log中的记录行并不全都真实存在. 
> 而是为了展示方便, 经过了少量的剪拼. (毕竟粘贴一个超大的read记录作为例子很不合适)

它可以单独解析一行数据:

```python
from sparce.record import SyscallRecord
from sparce.util.parse import parse_as

# SyscallRecord解析失败抛出SyscallParsingFailException异常(的子类)
sr = SyscallRecord('2652  1715524869.383394 [00007c77435968de] newfstatat(3, "", {st_mode=S_IFREG|0755, st_size=2220400, ...}, AT_EMPTY_PATH) = 0')

# parse_as相当于try expect return None, 不需要处理异常
sr = parse_as('2652  1715524869.383394 [00007c77435968de] newfstatat(3, "", {st_mode=S_IFREG|0755, st_size=2220400, ...}, AT_EMPTY_PATH) = 0'
              , SyscallRecord)

print(sr.syscall) # newfstatat
print(sr.status) # complete
print(sr.timestamp, sr.timestamp_format) # 1715524869.383394 epoch
print(sr.retval) # 0

# 是的, 下面的'...'只是个字符串
print(sr.arguments) # [(None, '3'), (None, '""'), ('st_mode', [(None, 'S_IFREG|0755'), ('st_size', '2220400'), (None, '...')]), (None, 'AT_EMPTY_PATH')]
```

能够在多行数据中匹配未完成和恢复的系统调用

```python
from sparce.util import parse_and_match_syscalls

complete_records, unfinished_records, resumed_records = parse_and_match_syscalls([
    '2651  1715524869.344040 [0000733108129d2b] mprotect(0x61a5b4ea3000, 8192, PROT_READ <unfinished ...>',
    '2649  1715524869.344116 [00007fd4e291986b] <... close resumed>) = 0',
    '2651  1715524869.344328 [0000733108129d2b] <... mprotect resumed>) = 0',
    '2649  1715524869.344425 [00007fd4e2927b3b] socket(AF_UNIX, SOCK_STREAM|SOCK_CLOEXEC|SOCK_NONBLOCK, 0 <unfinished ...>',
    '2651  1715524869.344626 [0000733108129d2b] mprotect(0x73310813b000, 8192, PROT_READ <unfinished ...>',
    '2649  1715524869.344723 [00007fd4e2927b3b] <... socket resumed>) = 5',
    '2651  1715524869.344912 [0000733108129d2b] <... mprotect resumed>) = 0',
    '2649  1715524869.345149 [00007fd4e29274f7] connect(5, {sa_family=AF_UNIX, sun_path="/var/run/nscd/socket"}, 110 <unfinished ...>',
    '2651  1715524869.345322 [0000733107f1a2e4] prlimit64(0, RLIMIT_STACK, NULL, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0',
    '2649  1715524869.345503 [00007fd4e29274f7] <... connect resumed>) = -1 ENOENT (No such file or directory)',
    '2649  1715524869.345739 [00007fd4e291986b] close(5 <unfinished ...>',
    '2651  1715524869.345917 [0000733108129cfb] munmap(0x7331080f0000, 67411 <unfinished ...>',
    '2651  1715524869.346464 [0000733107eec06b] getuid() = 1000',
    '2649  1715524869.344723 [00007fd4e2927b3b] <... socket resumed>) = 5',
])

print([str(_) for _ in complete_records])
"""
[
    '<SyscallRecord 1715524869.344040,epoch mprotect<complete> -> 0 3/3 arguments>', 
    '<SyscallRecord 1715524869.344425,epoch socket<complete> -> 5 3/3 arguments>', 
    '<SyscallRecord 1715524869.344626,epoch mprotect<complete> -> 0 3/3 arguments>', 
    '<SyscallRecord 1715524869.345322,epoch prlimit64<complete> -> 0 4/4 arguments>', 
    '<SyscallRecord 1715524869.345149,epoch connect<complete> -> ENOENT(-1) 3/3 arguments>', 
    '<SyscallRecord 1715524869.346464,epoch getuid<complete> -> 1000 0/0 arguments>'
]


"""

print([str(_) for _ in unfinished_records])
"""
[
    '<SyscallRecord 1715524869.345739,epoch close<unfinished> <no-return> 0/0 arguments>', 
    '<SyscallRecord 1715524869.345917,epoch munmap<unfinished> <no-return> 2/2 arguments>'
]
"""

print([str(_) for _ in resumed_records])
"""
[
    '<SyscallRecord 1715524869.344116,epoch close<resuming> -> 0 1/1 arguments>', 
    '<SyscallRecord 1715524869.344723,epoch socket<resuming> -> 5 1/1 arguments>'
]

"""
```

根据一些规则, 也能匹配信号量和非预期的跟踪情况
```python
from sparce.util.parse import parse_auto

syscall_records, signal_records, unexpected_records, failed_lines = parse_auto([
    '2652  1715524869.388965 [00007c77432425f3] rt_sigaction(SIGXFSZ, {sa_handler=0x643b23b05510, sa_mask=[HUP INT PIPE TERM XCPU XFSZ], sa_flags=SA_RESTORER, sa_restorer=0x7c7743242520}, NULL, 8) = 0',
    '2652  1715524869.389157 [00007c7743319f4a] ioctl(1, TCGETS, 0x7ffe827c7840) = -1 ENOTTY (Inappropriate ioctl for device)',
    '2652  1715524869.389324 [00007c7743313d3e] newfstatat(0, "", {st_mode=S_IFIFO|0600, st_size=0, ...}, AT_EMPTY_PATH) = 0',
    '2652  1715524869.397744 [00007c77433147e2] read(0, "", 4096) = 0',
    '2652  1715524869.399203 [00007c7743314f67] close(0) = 0',
    '2652  1715524869.399348 [00007c7743314f67] close(1) = 0',
    '2652  1715524869.399524 [00007c77432eac31] exit_group(0) = ?',
    '2652  1715524869.399862 [????????????????] +++ exited with 0 +++',
    '2651  1715524869.399958 [0000733107eea3ea] <... wait4 resumed>[{WIFEXITED(s) && WEXITSTATUS(s) == 0}], 0, NULL) = 2652',
    '2651  1715524869.400051 [0000733107eea3ea] --- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=2652, si_uid=1000, si_status=0, si_utime=1, si_stime=0} ---',
    '2651  1715524869.400140 [0000733107e42529] rt_sigreturn({mask=[]}) = 2652',
    '2651  1715524869.400274 [0000733107eea3ea] wait4(-1, 0x7ffe65fd9c3c, WNOHANG, NULL) = -1 ECHILD (No child processes)',
    '2651  1715524869.400407 [0000733107eeac31] exit_group(0) = ?',
    '2651  1715524869.400739 [????????????????] +++ exited with 0 +++',
    '2649  1715524869.401042 [00007fd4e28ea3ea] <... wait4 resumed>[{WIFEXITED(s) && WEXITSTATUS(s) == 0}], 0, NULL) = 2651',
    '2649  1715524869.401321 [00007fd4e28ea3ea] --- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=2651, si_uid=1000, si_status=0, si_utime=0, si_stime=0} ---',
    '2649  1715524869.401649 [00007fd4e291986b] close(1) = 0',
    '2649  1715524869.402514 [00007fd4e291986b] this-is-invalid-line :)', # 这有点小儿科, 但我一下子找不到更好的例子了
    '2649  1715524869.402561 [00007fd4e291986b] close(2) = 0',
    '2649  1715524869.403025 [00007fd4e28eac31] exit_group(0) = ?',
    '2649  1715524869.405065 [????????????????] +++ exited with 0 +++',
], _match_syscall=True)

print([str(_) for _ in syscall_records])

"""
[
    '<SyscallRecord 1715524869.388965,epoch rt_sigaction<complete> -> 0 4/4 arguments>', 
    '<SyscallRecord 1715524869.389157,epoch ioctl<complete> -> ENOTTY(-1) 3/3 arguments>', 
    '<SyscallRecord 1715524869.389324,epoch newfstatat<complete> -> 0 4/4 arguments>', 
    '<SyscallRecord 1715524869.397744,epoch read<complete> -> 0 3/3 arguments>', 
    '<SyscallRecord 1715524869.399203,epoch close<complete> -> 0 1/1 arguments>', 
    '<SyscallRecord 1715524869.399348,epoch close<complete> -> 0 1/1 arguments>', 
    '<SyscallRecord 1715524869.399524,epoch exit_group<complete> -> ? 1/1 arguments>', 
    '<SyscallRecord 1715524869.400140,epoch rt_sigreturn<complete> -> 2652 1/1 arguments>', 
    '<SyscallRecord 1715524869.400274,epoch wait4<complete> -> ECHILD(-1) 4/4 arguments>', 
    '<SyscallRecord 1715524869.400407,epoch exit_group<complete> -> ? 1/1 arguments>', 
    '<SyscallRecord 1715524869.401649,epoch close<complete> -> 0 1/1 arguments>', 
    '<SyscallRecord 1715524869.402561,epoch close<complete> -> 0 1/1 arguments>', 
    '<SyscallRecord 1715524869.403025,epoch exit_group<complete> -> ? 1/1 arguments>', 
    '<SyscallRecord 1715524869.399958,epoch wait4<resuming> -> 2652 3/3 arguments>', 
    '<SyscallRecord 1715524869.401042,epoch wait4<resuming> -> 2651 3/3 arguments>'
]

"""

print([str(_) for _ in signal_records])

"""
    [
        '<SignalRecord 1715524869.400051,epoch SIGCHLD>', 
        '<SignalRecord 1715524869.401321,epoch SIGCHLD>'
    ]
"""

print([str(_) for _ in unexpected_records])

"""
[
    '<UnexceptedRecord 1715524869.399862,epoch 0 exited>', 
    '<UnexceptedRecord 1715524869.400739,epoch 0 exited>', 
    '<UnexceptedRecord 1715524869.405065,epoch 0 exited>'
]

"""

print([str(_) for _ in failed_lines])

"""
    ['2649  1715524869.402514 [00007fd4e291986b] this-is-invalid-line :)']
"""
```

## design

关于这个小工具的实现思路见`doc/design/`, 例如[record-parsing](./design/record-parsing.md)