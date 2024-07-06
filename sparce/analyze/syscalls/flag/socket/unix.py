from enum import IntFlag, auto

class UnixSocketOption(IntFlag):
    """
       SO_PASSCRED
       SO_PASSSEC
       SO_PEEK_OFF
       SO_PEERCRED
       SO_PEERSEC
    """
    SO_PASSCRED = 1
    SO_PASSSEC = auto()
    SO_PEEK_OFF = auto()
    SO_PEERCRED = auto()
    SO_PEERSEC = auto()

class UnixAncillary(IntFlag):
    """
       SCM_RIGHTS
       SCM_CREDENTIALS
       SCM_SECURITY
    """
    SCM_RIGHTS = 1
    SCM_CREDENTIALS = auto()
    SCM_SECURITY = auto()