from enum import IntFlag
"""
       MSG_CONFIRM (since Linux 2.3.15)

       MSG_DONTROUTE

       MSG_DONTWAIT (since Linux 2.2)

       MSG_EOR (since Linux 2.2)

       MSG_MORE (since Linux 2.4.4)

       MSG_NOSIGNAL (since Linux 2.2)

       MSG_OOB

       MSG_FASTOPEN (since Linux 3.7)
"""

class SendFlag(IntFlag):
    MSG_CONFIRM = 0x0001
    MSG_DONTROUTE = 0x0002
    MSG_DONTWAIT = 0x0004
    MSG_EOR = 0x0008
    MSG_MORE = 0x0010
    MSG_NOSIGNAL = 0x0020
    MSG_OOB = 0x0040
    MSG_FASTOPEN = 0x0080
    