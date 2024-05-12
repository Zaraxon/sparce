import re


class Prefix:
    
    def process(self):

        line: str = self._line

        ### PID
        self.pid = None
        m = re.search('^\s*?([0-9]+)\s*', line)
        if m is not None:
            self.pid = m.group(1).strip()
            line = line[m.end():]
        else:
            m = re.search('^\s*\[pid ([0-9]+)\]\s*', line)
            if m is not None:
                self.pid = m.group(1).strip()
                line = line[m.end():]

        ### timestamp
        self.timestamp, self.timestamp_format = None, None

        ### 1 -t, wall clock time
        m = re.search('^\s*?([0-9]{2}):([0-9]{2}):([0-9]{2})\s*', line)
        if m is not None:
            self.timestamp = m.group().strip()
            self.timestamp_format = 'wallclock'
            line = line[m.end():]
        ### 2 -tt, wall clock time.ms
        m = re.search('^\s*([0-9]{2}):([0-9]{2}):([0-9]{2})\.([0-9]+)\s*', line)
        if m is not None and not self.timestamp:
            self.timestamp = m.group().strip()
            self.timestamp_format = 'wallclockms'
            line = line[m.end():]
        ### 3 -ttt epoch time
        m = re.search('^\s*[0-9]+\.[0-9]+\s*', line)
        if m is not None and not self.timestamp:
            self.timestamp = m.group().strip()
            self.timestamp_format = 'epoch'
            line = line[m.end():]

        
        ### instruction pointer
        self.instruction_pointer = None
        m = re.search('^\s*\[(([0-9a-zA-Z])+|(\?)+)\]\s*', line)
        if m is not None:
            self.instruction_pointer = m.group().strip()
            line = line[m.end():]
        
        self._prefix = self._line[:self._line.index(line)]
        self._line = line
        

    def to_string(
            self,
            pid=False,
            time=False
    ) -> str:
        
        to_string = ''
        
        if pid:
            to_string = f'<pid {self.pid}> ' + to_string
        if time:
            if self.timestamp:
                to_string = f'<{self.timestamp}, {self.timestamp_format}> ' + to_string
            else:
                to_string = f'<no-time> ' + to_string
        
        return to_string.strip()
