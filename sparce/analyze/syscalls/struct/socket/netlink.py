from ...flag.socket import socket
from ...flag.socket import NlMsgType, NlmsgFlag

"""
    struct sockaddr_nl {
        sa_family_t     nl_family;  /* AF_NETLINK */
        unsigned short  nl_pad;     /* Zero */
        pid_t           nl_pid;     /* Port ID */
        __u32           nl_groups;  /* Multicast groups mask */
    };
"""

class sockaddr_nl(tuple):

    @property
    def nl_family(self) -> socket.Domain:
        return self[0]
    
    @property
    def nl_pad(self) -> int:
        return self[1]
    
    @property
    def nl_pid(self) -> int:
        return self[2]
    
    @property
    def nl_groups(self) -> int:
        return self[3]
    
"""
           struct nlmsghdr {
               __u32 nlmsg_len;    /* Length of message including header */
               __u16 nlmsg_type;   /* Type of message content */
               __u16 nlmsg_flags;  /* Additional flags */
               __u32 nlmsg_seq;    /* Sequence number */
               __u32 nlmsg_pid;    /* Sender port ID */
           };
"""

class nlmsghdr(tuple):
    
    @property
    def nlmsg_len(self) -> int:
        return self[0]
    
    @property
    def nlmsg_type(self) -> NlMsgType:
        return self[1]
    
    @property
    def nlmsg_flags(self) -> NlmsgFlag:
        return self[2]
    
    @property
    def nlmsg_seq(self) -> int:
        return self[3]
    
    @property
    def nlmsg_pid(self) -> int:
        return self[4]

