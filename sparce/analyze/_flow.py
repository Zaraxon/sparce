from ..record import SyscallRecord


"""
    测试代码, 非正式
"""
def search_anyflow(records: list[SyscallRecord]) -> list[tuple[SyscallRecord]]:

    APPLY = [
        'open', 'creat', 'socket', 'mmap', 'mmap2', 'pipe', 
        'pipe2', 'shmget', 'semget', 'msgget', 'clone', 'clone2', 'clone3', 'fork', 'vfork',  
        'inotify_init', 'inotify_init1', 'fanotify_init', 'timerfd_create', 'eventfd', 'eventfd2', 
        'epoll_create', 'epoll_create1', 'signalfd', 'signalfd4', 'io_setup', 'mq_open', 
        'add_key', 'request_key', 'memfd_create', 'userfaultfd', 'pkey_alloc',  'io_uring_setup', 
        'open_tree', 'fsopen', 'pidfd_open', 'landlock_create_ruleset', 'set_tls' 
    ]
    RELEASE = [
        'close', 'shutdown', 'munmap', 'shmdt', 'shmctl', 'semctl', 'msgctl', 'exit', 'exit_group',  
        'unlink', 'rmdir', 'close_range', 'mq_unlink', 'io_destroy', 'pkey_free', 'io_uring_register', 
        'delete_module', 'landlock_add_rule', 'landlock_restrict_self'
    ]
    
    working, done = {}, []
    for r in records:
        if r.syscall in APPLY:
            if r.retval is not None:
                working[r.retval] = [r]
        elif r.syscall in RELEASE:
            for name, value in r.arguments:
                if isinstance(value, int) and value in working.keys():
                    working[value].append(r)
                    done.append(tuple(working.pop(value)))
                    break
        elif r.arguments:

            for name, value in r.arguments:
                if isinstance(value, int) and value in working.keys():
                    working[value].append(r)
                    break


    done += [tuple(_) for _ in working.values()]
    return done
                    