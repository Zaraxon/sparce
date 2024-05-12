
## Record
sparce/record 中为可以产生的

### SyscallRecord SyscallRecordNoArg

分别描述一条完整的系统调用信息, 和它的不解析参数版本.

**syscall**: `str`类型, 系统调用名

**status**: `str`类型, 记录的完成状态, 取值`complete`, `unfinished`, `resuming`.

**complete**, **unfinished**, **resuming**: `bool`类型, 同样描述完成状态

**arguments**(限SyscallRecord): `list`类型, 其中每个元素是一个`list`或`str`. 如果是`list`, 则其包括了strace对该参数内部元素的解析. 例子见[overview](./overview.md#quick-start)

[optional] **retval**, **errorcode**, **errordesc**: `str`类型, 描述返回状态.
例如"-1", "ENOENT", "No such file or directory". 

[optional] **timestamp**, **timestamp_format**: 时间戳, 依照[manpage](https://man7.org/linux/man-pages/man1/strace.1.html)中, `wallclock`(HH:MM:SS), `wallclockms`(HH:MM:SS.ms), `epoch`(1388536422.679099) 三种格式解析.

**\_\_str\_\_ -> str**: 记录的摘要方法, 用于打印到命令行. 区别于**to_serialized**

**to_serialized -> str**: 比较完整的记录信息, 用于打印到文件手动分析.

### SignalRecord

描述信号量

**signal**: `str`类型, 信号量名称, 例如`SIGTERM`

[optional] **timestamp**, **timestamp_format**: 时间戳, 依照[manpage](https://man7.org/linux/man-pages/man1/strace.1.html)中, `wallclock`(HH:MM:SS), `wallclockms`(HH:MM:SS.ms), `epoch`(1388536422.679099) 三种格式解析.

**\_\_str\_\_ -> str**: 同[SyscallRecord](./record.md#syscallrecord-syscallrecordnoarg)

**to_serialized -> str**: 同[SyscallRecord](./record.md#syscallrecord-syscallrecordnoarg)

### UnexpectedRecord

[manpage](https://man7.org/linux/man-pages/man1/strace.1.html)中的几种无法继续记录的情况, 常见的有退出(`exited`), 进程被杀死`killed`等. 

**type**: `str`类型, 异常情况名称, 详见`sparce/record/unexpected.py`中, `UnexceptedRecord.__PATTERNS__`的键. 

[optional] **pid**: `str`类型, 关联到的pid
[optional] **mode**: `str`类型, 与`[ Process PID=NNNN runs in PPP mode. ]`相关
