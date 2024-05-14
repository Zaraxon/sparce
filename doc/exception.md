## Exception

关于模块的异常处理. 

从任何Record类的子类直接构造时可能会抛出与解析失败相关的异常. 目前, 抛出什么异常和异常时正在解析的部分是绑定的. 例如:

在解析`SyscallRecord`过程中抛出`ResumingUnfinishedException`表示处理过程中遇到了类似`<unfinished ...> <... epoll_wait resumed>) = 0`的情况. 

而`SyscallParsingFailGeneralException`则表示任何未归类的解析失败的情况. 

如果不需要对每一种解析失败的情况进行细分的处理, 建议使用`util.parse`模块中的工具函数来创建这些Record类, 通常来说, 它们在解析/处理失败时要么:
1. 返回None
2. 过滤掉失败的部分, 只返回成功的
3. 将失败的部分单独返回