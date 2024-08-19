"""Main module for setting up a containerized environment using Linux namespaces."""

import ctypes
import os

import flags

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


def run() -> None:
    """
    Forks a new process, sets up a new namespace, and runs a BusyBox shell.

    This function forks the current process using `os.fork`. The child process
    then unshares the mount namespace, mounts a new `proc` filesystem, changes
    the root directory to `/myroot/`, and executes a BusyBox shell. The parent
    process waits for the child to finish, unmounts the `proc` filesystem, and
    prints the process ID and exit status.

    Raises
    ------
    OSError
        If any system call fails, this function may raise an OSError.

    Examples
    --------
    Run the function to create a new namespace and start a shell:

    >>> run()
    """
    pid = os.fork()

    if pid == 0:
        unshare(flags.CLONE_NEWNS)
        os.system("mount -t proc none /myroot/proc")
        os.chroot("/myroot/")
        os.chdir("/")
        os.execvp("/bin/busybox", ["/bin/busybox", "sh"])
    else:
        rid, status = os.waitpid(pid, 0)
        os.system("umount /myroot/proc")
        print(rid, status)


if __name__ == "__main__":
    run()
