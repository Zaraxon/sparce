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

class ArgumentsParsingError(Exception):
    """
        Arguments的任何解析失败
    """
    def __init__(self, line: str, *args: object) -> None:
        super().__init__(*args)
        self.line = line