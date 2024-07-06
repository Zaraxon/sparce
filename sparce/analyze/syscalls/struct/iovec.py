from typing import Any

"""
    from https://man7.org/linux/man-pages/man3/iovec.3type.html

    struct iovec {
        void   *iov_base;  /* Starting address */
        size_t  iov_len;   /* Size of the memory pointed to by iov_base. */
    };
"""

class iovec(tuple):

    @property
    def iov_base(self) -> bytes | Any:
        return self[0]
    
    @property
    def iov_len(self) -> int:
        return self[1]