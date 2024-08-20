"""Module define system namespace utilities."""

import ctypes

libc = ctypes.CDLL("libc.so.6", use_errno=True)


def unshare(flag: int) -> None:
    """
    Unshares the specified kernel namespace.

    This function is a Python wrapper around the `unshare` system call, which
    disassociates parts of the process execution context. It can be used to
    create new namespaces for a process.

    Parameters
    ----------
    flag : int
        The namespace flag to be unshared. Common flags include:
        - `CLONE_NEWNS`: to unshare the mount namespace.
        - `CLONE_NEWPID`: to unshare the PID namespace.
        - `CLONE_NEWNET`: to unshare the network namespace.
        - `CLONE_NEWUTS`: to unshare the UTS namespace (hostname).
        - `CLONE_NEWIPC`: to unshare the IPC namespace.
        - `CLONE_NEWUSER`: to unshare the user namespace.

    Raises
    ------
    OSError
        If the `unshare` system call fails, this function will raise an
        OSError with the appropriate error number.
    """
    result = libc.unshare(flag)

    if result < 0:
        err_no = ctypes.get_errno()
        print(err_no)


def set_hostname(name: str) -> None:
    """
    Set the hostname for the current namespace.

    Parameters
    ----------
    name : str
        The new hostname to be set for the UTS namespace.

    Raises
    ------
    OSError
        If the system call to set the hostname fails, an OSError will be raised.
    """
    result = libc.sethostname(name.encode(), len(name))

    if result < 0:
        err_no = ctypes.get_errno()
        print(err_no)
