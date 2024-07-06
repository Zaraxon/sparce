from enum import IntFlag

class RecvFlag(IntFlag):
    """
   The flags argument
       The flags argument is formed by ORing one or more of the
       following values:

       MSG_CMSG_CLOEXEC (recvmsg() only; since Linux 2.6.23)

       MSG_DONTWAIT (since Linux 2.2)

       MSG_ERRQUEUE (since Linux 2.2)

       MSG_OOB

       MSG_PEEK

       MSG_TRUNC (since Linux 2.2)

       MSG_WAITALL (since Linux 2.2)

    """
    MSG_CMSG_CLOEXEC = 0x40000000
    MSG_DONTWAIT = 0x40
    MSG_ERRQUEUE = 0x20
    MSG_OOB = 0x1
    MSG_PEEK = 0x2
    MSG_TRUNC = 0x8
    MSG_WAITALL = 0x10