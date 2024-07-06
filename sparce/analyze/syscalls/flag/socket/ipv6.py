from enum import IntFlag, auto

from .ip import IPProtocol


class IPv6SocketOption(IntFlag):
    """
       IPV6_ADDRFORM
       IPV6_ADD_MEMBERSHIP, IPV6_DROP_MEMBERSHIP
       IPV6_MTU
       IPV6_MTU_DISCOVER
       IPV6_MULTICAST_HOPS
       IPV6_MULTICAST_IF
       IPV6_MULTICAST_LOOP
       IPV6_RECVPKTINFO (since Linux 2.6.14)
       IPV6_RTHDR, IPV6_AUTHHDR, IPV6_DSTOPTS, IPV6_HOPOPTS,
       IPV6_FLOWINFO, IPV6_HOPLIMIT
       IPV6_RECVERR
       IPV6_ROUTER_ALERT
       IPV6_UNICAST_HOPS
       IPV6_V6ONLY (since Linux 2.4.21 and 2.6)
    """
    IPV6_ADDRFORM = 1
    IPV6_ADD_MEMBERSHIP = auto()
    IPV6_DROP_MEMBERSHIP = auto()
    IPV6_MTU = auto()
    IPV6_MTU_DISCOVER = auto()
    IPV6_MULTICAST_HOPS = auto()
    IPV6_MULTICAST_IF = auto()
    IPV6_MULTICAST_LOOP = auto()
    IPV6_RECVPKTINFO = auto()
    IPV6_RTHDR = auto()
    IPV6_AUTHHDR = auto()
    IPV6_DSTOPTS = auto()
    IPV6_HOPOPTS = auto()
    IPV6_FLOWINFO = auto()
    IPV6_HOPLIMIT = auto()
    IPV6_RECVERR = auto()
    IPV6_ROUTER_ALERT = auto()
    IPV6_UNICAST_HOPS = auto()
    IPV6_V6ONLY = auto()

class IPv6Protocol(IntFlag):
    
    IPPROTO_TCP = 1
    IPPROTO_UDP = auto()
    IPPROTO_SCTP = auto()
    IPPROTO_UDPLITE = auto()
    IPPROTO_IPV6 = auto()