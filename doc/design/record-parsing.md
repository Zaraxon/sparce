## Record Parsing
将strace line处理为Record.

处理依据一个内部的状态机: `self._line`.
在类初始化时, 将`self._line`设置为strace line, 然后依据继承关系递归地处理. 
状态转换函数为`process`, 它读取当前的`self._line`, 从其中解析出一些信息, 最后将`self._line`设置为新的值, 供后续处理使用. 一般来说, `process`函数做的事情是从原始的`self._line`中"剥除"掉它需要的那部分. 

递归的状态转换过程依赖于类的继承顺序. 形式化地讲, 这一过程**后序遍历**某个Record的类的继承关系图(的实现了`process`的部分), 并依次调用每个`process`函数.

### example

举例来说, 对于`SyscallRecord`, 它的继承关系是:
```python
class SyscallRecord(SyscallRecordNoArg, Arguments):
    ...
class SyscallRecordNoArg(Record, Prefix, CompletionStatus, SyscallSuffix, SyscallFrame):
    ...
```
那么解析过程将首先检查`SyscallRecordNoArg`是否实现了`process`函数, 它实现了, 那么进入`SyscallRecordNoArg`.

然后依次检查`Record, Prefix, CompletionStatus, SyscallSuffix, SyscallFrame`, 是否有`process`的实现, 如果有则继续进入. 

进入到它们之中任何一个后, 不再有父类实现了`process`, 那么在退出到`SyscallRecordNoArg`前, 它们自己的`process`被依次调用. 然后退出到`SyscallRecordNoArg`, 调用`SyscallRecordNoArg.process`

最后, 类似地, `Argument.process`被调用, `SyscallRecord.process`最后被调用.

最终的调用顺序是
1. `Record`没有实现`process`
2. `Prefix`, 剥除时间戳等前缀
3. `CompletionStatus`, 剥除`<unfinished ...>`, `<... xxx resumed>`, 等后缀
4. `SyscallSuffix`, 剥除` = -1 ENOENT (No Such File or Directory)`这样的返回信息
5. `SyscallFrame`, 剥除`mmap2(...)`这个外壳, 暴露出里面的参数
6. `SyscallRecordNoArg`, 仅仅是一些检查
7. `Argument`, 处理剩下所有的参数. 

### parsing structured data with ply

在strace的man手册中大致列举了strace输出的log中如何表示system call的各种参数(整数, 字符串, iovec, etc.). sparce主要使用ply(python lex & yacc) 解析strace log中包含结构化数据的部分.

> 在这个项目的早期版本, 对于system call中被decoder解析出来的部分是通过(小心翼翼地)括号匹配逐步解析出一层层结构的. 但这种做法在扩展到全部system call或QEMU_STRACE这样不十分标准的输出格式时遇到了不少麻烦.

作为LALR解析器, ply允许构建整数, 字符串, 左大括号, 逗号等基本元素的lexer, 然后将lexer解析出的一个个token根据parser中定义的规则进行移进/归约, 组成结构化的python原语. 