import re

from .....record.prop import PropertyConstructionError

def htons(s: str) -> int:
    m = re.search(r'htons\((?P<htons>[0-9]+)\)', s)
    if m is None:
        raise PropertyConstructionError(f'Could not constructing htons: {s}')
    return int(m.group('htons'))

def htonl(s: str) -> int:
    m = re.search(r'htons\((?P<htonl>[0-9]+)\)', s)
    if m is None:
        raise PropertyConstructionError(f'Could not constructing htons: {s}')
    return int(m.group('htonl'))