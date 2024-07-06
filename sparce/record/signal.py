import re

from .record import Record
from .prefix import Prefix
from .arguments import Arguments


class SignalParsingFailException(Exception):

    def __init__(self, line: str, *args: object) -> None:
        super().__init__(*args)
        self.line = line

class SignalFrame:

    def process(self):
        line: str = self._line

        pattern = {
            'SIGNAL': '|'.join(self.SIGNALS).replace('+','\+').replace('-','\-'),
            'ARGUMENTS': r'\{.*?\}'
        }

        m = re.search(f'^\s*\-\-\-\s*(?P<SIGNAL>{pattern["SIGNAL"]})\s*(?P<ARGUMENTS>{pattern["ARGUMENTS"]})?\s*\-\-\-\s*$', line)

        if m is not None:
            self.signal = m.group('SIGNAL')
            if 'ARGUMENTS' in m.groupdict():
                self._line = m.group('ARGUMENTS')[1:-1].strip()

        if not hasattr(self, 'signal') or getattr(self, 'signal') is None:
            raise SignalParsingFailException(line=line)

class SignalRecord(Record, Prefix, SignalFrame, Arguments):

    SIGNALS = [
        'SIGHUP', 'SIGINT', 'SIGQUIT', 'SIGILL', 'SIGTRAP', 
        'SIGABRT', 'SIGBUS', 'SIGFPE', 'SIGKILL', 'SIGUSR1', 
        'SIGSEGV', 'SIGUSR2', 'SIGPIPE', 'SIGALRM', 'SIGTERM', 
        'SIGSTKFLT', 'SIGCHLD', 'SIGCONT', 'SIGSTOP', 'SIGTSTP', 
        'SIGTTIN', 'SIGTTOU', 'SIGURG', 'SIGXCPU', 'SIGXFSZ', 
        'SIGVTALRM', 'SIGPROF', 'SIGWINCH', 'SIGIO', 'SIGPWR', 
        'SIGSYS', 'SIGRTMIN', 'SIGRTMIN+1', 'SIGRTMIN+2', 'SIGRTMIN+3', 
        'SIGRTMIN+4', 'SIGRTMIN+5', 'SIGRTMIN+6', 'SIGRTMIN+7', 'SIGRTMIN+8', 
        'SIGRTMIN+9', 'SIGRTMIN+10', 'SIGRTMIN+11', 'SIGRTMIN+12', 'SIGRTMIN+13', 
        'SIGRTMIN+14', 'SIGRTMIN+15', 'SIGRTMAX-14', 'SIGRTMAX-13', 'SIGRTMAX-12', 
        'SIGRTMAX-11', 'SIGRTMAX-10', 'SIGRTMAX-9', 'SIGRTMAX-8', 'SIGRTMAX-7', 
        'SIGRTMAX-6', 'SIGRTMAX-5', 'SIGRTMAX-4', 'SIGRTMAX-3', 'SIGRTMAX-2', 
        'SIGRTMAX-1', 'SIGRTMAX'
    ]

    def process(self) -> None:
        
        if not hasattr(self, 'signal'):
            raise SignalParsingFailException(line=self.origin_line)

    
    def __str__(self) -> str:
        return f'<SignalRecord {self.to_string().strip()}>'
    
    def to_string(self) -> str:
        to_string = ''
        if self.timestamp:
            to_string += f'{self.timestamp},{self.timestamp_format}'
        if self.signal:
            to_string += ' ' + self.signal
        return to_string
    
    def to_serialized(self) -> str:
        to_string = ''
        if self.timestamp:
            to_string += f'{self.timestamp},{self.timestamp_format}'
        if self.signal:
            to_string += ' ' + self.signal
        return to_string + Arguments.to_serialized(self)
  