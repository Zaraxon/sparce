

class UnknownRecordException(Exception):

    def __init__(self, line: str, *args: object) -> None:
        super().__init__(*args)
        self.line = line

def _do_process(obj: object, cls: type=None) -> None:

    for base in cls.__bases__:
        if hasattr(base, 'process'):
            _do_process(obj, base)

    if hasattr(obj, 'process'):
        cls.process(obj)


class Record:

    def __init__(self, line: str) -> None:

        self.origin_line = self._line = line
        _do_process(self, self.__class__)
        
        

