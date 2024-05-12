import re

from .record import Record
from .prefix import Prefix

class UnexpectedParsingFailException(Exception):

    def __init__(self, line: str, *args: object) -> None:
        super().__init__(*args)
        self.line = line

class UnexceptedRecord(Record, Prefix):

    __PATTERNS__ = {
        'attached': '^\s*\[ Process ([0-9]+) attached \]\s*$',
        'detached': '^\s*\[ Process ([0-9]+) detached \]\s*$',
        'exited': '^\s*\+\+\+ exited with ([0-9]+) \+\+\+\s*$',
        'killed': '^\s*\+\+\+ killed by ([0-9A-Z]+) \+\+\+\s*$', 
        'stopped': '^\s*\-\-\- stopped by ([0-9A-Z]+) \-\-\-\s*$', 
        'superseded': '^\s*\+\+\+ superseded by execve in pid ([0-9]+) \+\+\+\s*$',
        'personality': '^\s*\[ Process PID=([0-9]+) runs in ([0-9]+) mode\. \]\s*$'
    }

    def process(self) -> None:
        
        line = self._line

        m = re.search(self.__PATTERNS__['attached'], line)
        if m is not None:
            self.type = 'attached'
            self.pid = m.group(1)
            self._line = ''
        
        m = re.search(self.__PATTERNS__['detached'], line)
        if m is not None:
            self.type = 'detached'
            self.pid = m.group(1).strip()
            self._line = ''
        
        m = re.search(self.__PATTERNS__['exited'], line)
        if m is not None:
            self.type = 'exited'
            self.pid = m.group(1).strip()
            self._line = ''

        m = re.search(self.__PATTERNS__['killed'], line)
        if m is not None:
            self.type = 'killed'
            self.pid = m.group(1).strip()
            self._line = ''
        
        m = re.search(self.__PATTERNS__['stopped'], line)
        if m is not None:
            self.type = 'stopped'
            self.pid = m.group(1).strip()
            self._line = ''

        m = re.search(self.__PATTERNS__['personality'], line)
        if m is not None:
            self.type = 'personality'
            self.pid = m.group(1).strip()
            self.mode = m.group(2).strip()
            self._line = ''

        if not hasattr(self, 'type'):
            raise UnexpectedParsingFailException(self._line)

    def __str__(self) -> str:
        return f'<UnexceptedRecord {self.to_string().strip()}>'
    
    def to_string(self) -> str:
        to_string = ''
        if self.timestamp:
            to_string += f'{self.timestamp},{self.timestamp_format}'
        if self.type and self.pid:
            to_string += ' ' + self.pid + ' ' + self.type
        return to_string
    
    def to_serialized(self) -> str:
        return self.to_string()
  
  