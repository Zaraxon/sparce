from enum import IntFlag, auto

class NetLinkFamily(IntFlag):
    """
       NETLINK_ROUTE
       NETLINK_W1 (Linux 2.6.13 to Linux 2.16.17)
       NETLINK_USERSOCK
       NETLINK_FIREWALL (up to and including Linux 3.4)
       NETLINK_SOCK_DIAG (since Linux 3.3)
       NETLINK_INET_DIAG (since Linux 2.6.14)
       NETLINK_NFLOG (up to and including Linux 3.16)
       NETLINK_XFRM
       NETLINK_SELINUX (since Linux 2.6.4)
       NETLINK_ISCSI (since Linux 2.6.15)
       NETLINK_AUDIT (since Linux 2.6.6)
       NETLINK_FIB_LOOKUP (since Linux 2.6.13)
       NETLINK_CONNECTOR (since Linux 2.6.14)
       NETLINK_NETFILTER (since Linux 2.6.14)
       NETLINK_SCSITRANSPORT (since Linux 2.6.19)
       NETLINK_RDMA (since Linux 3.0)
       NETLINK_IP6_FW (up to and including Linux 3.4)
       NETLINK_DNRTMSG
       NETLINK_KOBJECT_UEVENT (since Linux 2.6.10)
       NETLINK_GENERIC (since Linux 2.6.15)
       NETLINK_CRYPTO (since Linux 3.2)
    """
    NETLINK_ROUTE = 1
    NETLINK_USERSOCK = auto()
    NETLINK_FIREWALL = auto()
    NETLINK_SOCK_DIAG = auto()
    NETLINK_INET_DIAG = auto()
    NETLINK_NFLOG = auto()
    NETLINK_XFRM = auto()
    NETLINK_SELINUX = auto()
    NETLINK_ISCSI = auto()
    NETLINK_AUDIT = auto()
    NETLINK_FIB_LOOKUP = auto()
    NETLINK_CONNECTOR = auto()
    NETLINK_NETFILTER = auto()
    NETLINK_SCSITRANSPORT = auto()
    NETLINK_RDMA = auto()
    NETLINK_IP6_FW = auto()
    NETLINK_DNRTMSG = auto()
    NETLINK_KOBJECT_UEVENT = auto()
    NETLINK_GENERIC = auto()
    NETLINK_CRYPTO = auto()

class NlmsgFlag(IntFlag):
    """
       Standard flag bits in nlmsg_flags
       ──────────────────────────────────────────────────────────────────
       NLM_F_REQUEST           Must be set on all request messages.
       NLM_F_MULTI             The message is part of a multipart
                               message terminated by NLMSG_DONE.
       NLM_F_ACK               Request for an acknowledgement on
                               success.
       NLM_F_ECHO              Echo this request.
       Additional flag bits for GET requests
       ──────────────────────────────────────────────────────────────────
       NLM_F_ROOT               Return the complete table instead of a
                                single entry.
       NLM_F_MATCH              Return all entries matching criteria
                                passed in message content.  Not
                                implemented yet.
       NLM_F_ATOMIC             Return an atomic snapshot of the table.
       NLM_F_DUMP               Convenience macro; equivalent to
                                (NLM_F_ROOT|NLM_F_MATCH).

       Note that NLM_F_ATOMIC requires the CAP_NET_ADMIN capability or
       an effective UID of 0.
       Additional flag bits for NEW requests
       ──────────────────────────────────────────────────────────────────
       NLM_F_REPLACE             Replace existing matching object.
       NLM_F_EXCL                Don't replace if the object already
                                 exists.
       NLM_F_CREATE              Create object if it doesn't already
                                 exist.
       NLM_F_APPEND              Add to the end of the object list.
       """
        
    NLM_F_REQUEST = 1
    NLM_F_MULTI = auto()
    NLM_F_ACK = auto()
    NLM_F_ECHO = auto()
    NLM_F_ROOT = auto()
    NLM_F_MATCH = auto()
    NLM_F_ATOMIC = auto()
    NLM_F_DUMP = auto()
    NLM_F_REPLACE = auto()
    NLM_F_EXCL = auto()
    NLM_F_CREATE = auto()
    NLM_F_APPEND = auto()

class NlMsgType(IntFlag):
    """
       nlmsg_type can be one of the standard message types: NLMSG_NOOP
       message is to be ignored, NLMSG_ERROR message signals an error
       and the payload contains an nlmsgerr structure, NLMSG_DONE
       message terminates a multipart message. 
    """
    
    NLMSG_NOOP = 1
    NLMSG_ERROR = auto()
    NLMSG_DONE = auto()

class NetlinkSocketOption(IntFlag):
    """
       NETLINK_PKTINFO (since Linux 2.6.14)
       NETLINK_ADD_MEMBERSHIP
       NETLINK_DROP_MEMBERSHIP (since Linux 2.6.14)
       NETLINK_LIST_MEMBERSHIPS (since Linux 4.2)
       NETLINK_BROADCAST_ERROR (since Linux 2.6.30)
       NETLINK_NO_ENOBUFS (since Linux 2.6.30)
       NETLINK_LISTEN_ALL_NSID (since Linux 4.2)
       NETLINK_CAP_ACK (since Linux 4.3)
    """
    
    NETLINK_PKTINFO = 1
    NETLINK_ADD_MEMBERSHIP = auto()
    NETLINK_DROP_MEMBERSHIP = auto()
    NETLINK_LIST_MEMBERSHIPS = auto()
    NETLINK_BROADCAST_ERROR = auto()
    NETLINK_NO_ENOBUFS = auto()
    NETLINK_LISTEN_ALL_NSID = auto()
    NETLINK_CAP_ACK = auto()
