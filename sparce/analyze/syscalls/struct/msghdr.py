from typing import Any

from .iovec import iovec


"""
    struct msghdr {
        void         *msg_name;       /* Optional address */
        socklen_t     msg_namelen;    /* Size of address */
        struct iovec *msg_iov;        /* Scatter/gather array */
        size_t        msg_iovlen;     /* # elements in msg_iov */
        void         *msg_control;    /* Ancillary data, see below */
        size_t        msg_controllen; /* Ancillary data buffer len */
        int           msg_flags;      /* Flags (unused) */
    };

"""
class msghdr(tuple):

    @property
    def msg_name(self) -> Any:
        return self[0]
    
    @property
    def msg_namelen(self) -> int:
        return self[1]
    
    @property
    def msg_iov(self) -> iovec:
        return self[2]
    
    @property
    def msg_iovlen(self) -> int:
        return self[3]
    
    @property
    def msg_control(self) -> Any:
        raise NotImplementedError()
    
    @property
    def msg_controllen(self) -> int:
        raise NotImplementedError()

"""
    struct mmsghdr {
        struct msghdr msg_hdr;  /* Message header */
        unsigned int  msg_len;  /* Number of bytes transmitted */
    };
"""
class mmsghdr(tuple):

    @property
    def msg_hdr(self) -> msghdr:
        return self[0]
    
    @property
    def msg_len(self) -> int:
        return self[1]