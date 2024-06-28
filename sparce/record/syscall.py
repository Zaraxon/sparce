import re
import errno

from .record import Record
from .prefix import Prefix
from .arguments import Arguments


class SyscallParsingFailException(Exception):

    def __init__(self, line: str, *args: object) -> None:
        super().__init__(*args)
        self.line = line

class SyscallParsingFailGeneralException(SyscallParsingFailException):
    """
        任何没有考虑到的异常
    """

    def __init__(self, line: str, *args: object) -> None:
        super().__init__(line, *args)

class ResumingUnfinishedException(SyscallParsingFailException):
    """
        先resume又unfinished,暂时无法解析.  
    """

    def __init__(self, syscall: str, line: str, *args: object) -> None:
        super().__init__(line, *args)
        self.syscall = syscall


class SyscallSuffix:
    """
        
        提取返回值, 错误码, 和对错误的解释

        补充: -T syscall时间, 针对_newselect的(in ..., left ...)

    """
    ERROR_CODES = list(errno.errorcode.values()) + ['ERESTARTSYS', 'ECONNREFUSED']

    def process(self):

        line: str = self._line

        self.retval, self.errorcode, self.errordesc = None, None, None

        _eq = line.rfind('=')
        if _eq >= 0:
            line = line[_eq+1:]
        else:
            return
        
        patterns = {
            'RETVAL': '(0x0|0|00|(\-?[1-9][0-9]*))|(\-?0x[1-9a-fA-F][0-9a-fA-F]*)|(\-?0[1-7][0-7]*)|(\?)',
            'SELECTINFO': '\(in\s*\[[0-9]+\](,\s*left\s*\{[0-9]+,\s*[0-9]+\})*\)',
            'SYSCALLTIME': '<[0-9]+\.[0-9]+>',
            'ERRORCODE': '|'.join(self.ERROR_CODES),
            'ERRORDESC': '\((?!in).*?\)'
        }
        pattern = f'^\s*(?P<RETVAL>{patterns["RETVAL"]})\s*(?P<ERRORCODE>{patterns["ERRORCODE"]})?\s*(?P<ERRORDESC>{patterns["ERRORDESC"]})?\s*(?P<SELECTINFO>{patterns["SELECTINFO"]})?\s*(?P<SYSCALLTIME>{patterns["SYSCALLTIME"]})?\s*$'
        m = re.search(pattern, line)
        if m is not None:
            d = m.groupdict()
            self.retval, self.errorcode, self.errordesc, self._selectinfo, self.syscall_time = \
                d.get('RETVAL'), d.get('ERRORCODE'), d.get('ERRORDESC'), d.get('SELECTINFO'), d.get('SYSCALLTIME')
            if any((self.retval, self.errorcode, self.errordesc, self._selectinfo, self.syscall_time)):
                self._line = self._line[:_eq]

class CompletionStatus:
    """

        摘掉<unfinished ...>和<... xxx resumed>, 并从中提取调用名(如果有)

    """

    def process(self):
        
        line = self._line
        
        patterns = {
            'UNFNINISHED': '<unfinished ...>',
            'RESUMING': '|'.join(self.SYSCALLS)
        }
        
        self.former, self.latter = True, True
        m = re.search(f'(<... (?P<RESUMING>{patterns["RESUMING"]}) resumed>)', line)
        if m is not None:
            d = m.groupdict()

            self.former, self.latter = False, True
            self._line = line[m.end():]
            self.syscall = d.get('RESUMING')

            # FIXME: 这种情况目前视为解析失败:
            #    [一些数据] <... _newselect resumed> <unfinished ...> [一些数据]
            m = re.search(f'(?P<UNFNINISHED>{patterns["UNFNINISHED"]})', line)
            if m is not None:
                raise ResumingUnfinishedException(self.syscall, self.origin_line)

        else:
            m = re.search(f'(?P<UNFNINISHED>{patterns["UNFNINISHED"]})', line)
            if m is not None:
                d = m.groupdict()
                self.former, self.latter = True, False
                self._line = line[:m.start()]            

class SyscallFrame:
    """
        
        剥去调用外壳并寻找名字

    """

    def process(self):

        line: str = self._line.strip()

        ### 找名字并剥除外壳
        if self.unfinished or self.complete:
            for syscall in self.SYSCALLS:
                if line.startswith(f'{syscall}('):
                    self.syscall = syscall
                    break
            if not hasattr(self, 'syscall'):
                raise SyscallParsingFailGeneralException(self.origin_line)
            line = line[len(f'{self.syscall}('): len(line)-len(')')]
            self._line = line   
        elif self.resuming:
            pass # 这部分在CompletionStatus做了
            if not hasattr(self, 'syscall'):
                raise SyscallParsingFailGeneralException(self.origin_line)

class SyscallRecordNoArg(Record, Prefix, CompletionStatus, SyscallSuffix, SyscallFrame):

    SYSCALLS = [
        'read', 'write', 'open', 'close', 'stat', 'fstat', 'lstat', 'poll', 'lseek', 'mmap', 'mmap2', 'mprotect', 'munmap', 
        'brk', 'rt_sigaction', 'rt_sigprocmask', 'rt_sigreturn', 'ioctl', 'pread64', 'pwrite64', 'readv', 'writev', 'access', 
        'pipe', 'pipe2', 'select', 'pselect6', 'sched_yield', 'mremap', 'msync', 'mincore', 'madvise', 'shmget', 'shmat', 
        'send', 'recv', 'lstat64', 'ftruncate64', '_newselect', '_llseek', 
        'shmctl', 'dup', 'dup2', 'dup3', 'pause', 'nanosleep', 'getitimer', 'alarm', 'setitimer', 'getpid', 'sendfile', 
        'sendfile64', 'socket', 'connect', 'accept', 'accept4', 'sendto', 'recvfrom', 'sendmsg', 'recvmsg', 'shutdown', 
        'bind', 'listen', 'getsockname', 'getpeername', 'socketpair', 'setsockopt', 'getsockopt', 'clone', 'clone2', 'clone3', 
        'fork', 'vfork', 'execve', 'exit', 'exit_group', 'wait4', 'kill', 'uname', 'semget', 'semop', 'semctl', 'shmdt', 
        'msgget', 'msgsnd', 'msgrcv', 'msgctl', 'fcntl', 'flock', 'fsync', 'fdatasync', 'truncate', 'ftruncate', 'getdents', 
        'getdents64', 'getcwd', 'chdir', 'fchdir', 'rename', 'mkdir', 'rmdir', 'creat', 'link', 'unlink', 'symlink', 
        'readlink', 'chmod', 'fchmod', 'chown', 'fchown', 'lchown', 'umask', 'gettimeofday', 'getrlimit', 'getrusage', 
        'sysinfo', 'times', 'ptrace', 'getuid', 'syslog', 'getgid', 'setuid', 'setgid', 'geteuid', 'getegid', 'setpgid', 
        'getppid', 'getpgrp', 'setsid', 'setreuid', 'setregid', 'getgroups', 'setgroups', 'setresuid', 'getresuid', 'setresgid', 
        'getresgid', 'getpgid', 'setfsuid', 'setfsgid', 'getsid', 'capget', 'capset', 'rt_sigpending', 'rt_sigtimedwait', 
        'rt_sigqueueinfo', 'rt_sigsuspend', 'sigaltstack', 'utime', 'mknod', 'uselib', 'personality', 'ustat', 'statfs', 
        'fstatfs', 'sysfs', 'getpriority', 'setpriority', 'sched_setparam', 'sched_getparam', 'sched_setscheduler', 
        'sched_getscheduler', 'sched_get_priority_max', 'sched_get_priority_min', 'sched_rr_get_interval', 'mlock', 
        'munlock', 'mlockall', 'munlockall', 'vhangup', 'modify_ldt', 'pivot_root', '_sysctl', 'prctl', 'arch_prctl', 
        'adjtimex', 'setrlimit', 'chroot', 'sync', 'acct', 'settimeofday', 'mount', 'umount2', 'swapon', 'swapoff', 
        'reboot', 'sethostname', 'setdomainname', 'iopl', 'ioperm', 'create_module', 'init_module', 'delete_module', 
        'get_kernel_syms', 'query_module', 'quotactl', 'nfsservctl', 'getpmsg', 'putpmsg', 'afs_syscall', 'tuxcall', 
        'security', 'gettid', 'readahead', 'setxattr', 'lsetxattr', 'fsetxattr', 'getxattr', 'lgetxattr', 'fgetxattr', 
        'listxattr', 'llistxattr', 'flistxattr', 'removexattr', 'lremovexattr', 'fremovexattr', 'tkill', 'time', 
        'futex', 'sched_setaffinity', 'sched_getaffinity', 'set_thread_area', 'io_setup', 'io_destroy', 'io_getevents', 
        'io_submit', 'io_cancel', 'get_thread_area', 'lookup_dcookie', 'epoll_create', 'epoll_ctl_old', 'epoll_wait_old', 
        'remap_file_pages', 'getdents64', 'set_tid_address', 'restart_syscall', 'semtimedop', 'fadvise64', 'timer_create', 
        'timer_settime', 'timer_gettime', 'timer_getoverrun', 'timer_delete', 'clock_settime', 'clock_gettime', 
        'clock_getres', 'clock_nanosleep', 'exit_group', 'epoll_wait', 'epoll_ctl', 'tgkill', 'utimes', 'vserver', 
        'mbind', 'set_mempolicy', 'get_mempolicy', 'mq_open', 'mq_unlink', 'mq_timedsend', 'mq_timedreceive', 'mq_notify', 
        'mq_getsetattr', 'kexec_load', 'waitid', 'add_key', 'request_key', 'keyctl', 'ioprio_set', 'ioprio_get', 'inotify_init', 
        'inotify_add_watch', 'inotify_rm_watch', 'migrate_pages', 'openat', 'mkdirat', 'mknodat', 'fchownat', 'futimesat', 
        'newfstatat', 'unlinkat', 'renameat', 'linkat', 'symlinkat', 'readlinkat', 'fchmodat', 'faccessat', 'pselect6', 
        'ppoll', 'unshare', 'set_robust_list', 'get_robust_list', 'splice', 'tee', 'sync_file_range', 'vmsplice', 'move_pages', 
        'utimensat', 'epoll_pwait', 'signalfd', 'timerfd_create', 'eventfd', 'fallocate', 'timerfd_settime', 'timerfd_gettime', 
        'accept4', 'signalfd4', 'eventfd2', 'epoll_create1', 'dup3', 'pipe2', 'inotify_init1', 'preadv', 'pwritev', 
        'rt_tgsigqueueinfo', 'perf_event_open', 'recvmmsg', 'fanotify_init', 'fanotify_mark', 'prlimit64', 'name_to_handle_at', 
        'open_by_handle_at', 'clock_adjtime', 'syncfs', 'sendmmsg', 'setns', 'getcpu', 'process_vm_readv', 'process_vm_writev', 
        'kcmp', 'finit_module', 'sched_setattr', 'sched_getattr', 'renameat2', 'seccomp', 'getrandom', 'memfd_create', 'kexec_file_load', 
        'bpf', 'execveat', 'userfaultfd', 'membarrier', 'mlock2', 'copy_file_range', 'preadv2', 'pwritev2', 'pkey_mprotect', 'pkey_alloc', 
        'pkey_free', 'statx', 'io_pgetevents', 'rseq', 'pidfd_send_signal', 'io_uring_setup', 'io_uring_enter', 'io_uring_register', 
        'open_tree', 'move_mount', 'fsopen', 'fsconfig', 'fsmount', 'fspick', 'pidfd_open', 'clone3', 'close_range', 'openat2', 
        'pidfd_getfd', 'faccessat2', 'process_madvise', 'epoll_pwait2', 'mount_setattr', 'landlock_create_ruleset', 'landlock_add_rule', 
        'landlock_restrict_self', 'fstat64', 'stat64', 'set_tls', 'ugetrlimit', 'fcntl64', 'waitpid'
    ]

    def process(self) -> None:
        if not hasattr(self, 'syscall'):
            raise SyscallParsingFailGeneralException(self.origin_line)
    
    def __str__(self) -> str:
        return f'<SyscallRecordNoArg {self.to_string()}>'
    
    def merge(self, other):

        if not isinstance(other, self.__class__):
            return None
        if self.syscall != other.syscall:
            return None
        
        if self.unfinished and other.resuming:
            former, latter = self, other
        elif other.unfinished and self.resuming:
            former, latter = other, self
        else:
            return None
        
        newline = former.origin_line[:former.origin_line.index('<unfinished ...>')] + \
            latter.origin_line[latter.origin_line.index('resumed>')+len('resumed>'):]
        return self.__class__(newline)

    def to_string(
            self,
            suffix=True,
    ):
        to_string = ''
        if self.timestamp:
            to_string += f'{self.timestamp},{self.timestamp_format}'
        to_string += f' {self.syscall}'
        to_string += f'<{self.status}>'
        if suffix:
            if not any((self.retval, self.errorcode, self.errordesc)):
                to_string += f' <no-return>'
            else:
                to_string += f' -> '
                if self.errorcode is None:
                    if self.retval:
                        to_string += f'{self.retval}'
                    else:
                        to_string += '?'
                else :
                    to_string += f'{self.errorcode}({self.retval})'

        return to_string

    def to_serialized(self):
        ### TODO: 这里应该和to_string逻辑分开
        return self.to_string()

    @property
    def unfinished(self) -> bool:
        return (self.former is True) and (self.latter is False)
    
    @property
    def resuming(self) -> bool:
        return (self.former is False) and (self.latter is True)
    
    @property
    def complete(self) -> bool:
        return (self.former is True) and (self.latter is True)
    
    @property
    def status(self) -> str:
        return 'complete' if self.complete else ('unfinished' if self.unfinished else 'resuming')

class SyscallRecord(SyscallRecordNoArg, Arguments):
    
    def __str__(self) -> str:
        return f'<SyscallRecord {self.to_string().strip()}>'
    
    def to_string(self):
        return SyscallRecordNoArg.to_string(self) + ' ' + f'{Arguments.to_string(self)}'
    
    def to_serialized(self):
        return SyscallRecordNoArg.to_serialized(self) + ' ' + Arguments.to_serialized(self)
