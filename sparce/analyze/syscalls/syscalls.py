from ...record import SyscallRecord

from .prop import *

class Open(SyscallRecord, OpenProperties):
    pass
class Close(SyscallRecord, CloseProperties):
    pass
class Read(SyscallRecord, ReadProperties):
    pass
class Write(SyscallRecord, WriteProperties):
    pass
class Socket(SyscallRecord, SocketProperties):
    pass
class Connect(SyscallRecord, ConnectProperties):
    pass
class Accept(SyscallRecord, AcceptProperties):
    pass
class Bind(SyscallRecord, BindProperties):
    pass
class Send(SyscallRecord, SendProperties):
    pass
class Recv(SyscallRecord, RecvProperties):
    pass
class SendTo(SyscallRecord, SendToProperties):
    pass
class RecvFrom(SyscallRecord, RecvFromProperties):
    pass
class SendMsg(SyscallRecord, SendMsgProperties):
    pass
class RecvMsg(SyscallRecord, RecvMsgProperties):
    pass
class SendMMsg(SyscallRecord, SendMMsgProperties):
    pass
class RecvMMsg(SyscallRecord, RecvMMsgProperties):
    pass
class Dup(SyscallRecord, DupProperties):
    pass
class Dup2(SyscallRecord, Dup2Properties):
    pass