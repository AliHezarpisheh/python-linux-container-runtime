"""Main module for setting up a containerized environment using Linux namespaces."""

import ctypes
import os

import flags
from groups import create_control_group
from namespaces import libc, set_hostname, unshare


def run_child_proc() -> None:
    """
    Child process routine for setting up the container environment.

    This function is executed by the child process created through `libc.clone`.
    It performs the following tasks:
    1. Creates a control group for the process.
    2. Unshares the mount and UTS namespaces for isolation.
    3. Sets the hostname to "my-container".
    4. Mounts a new `proc` filesystem at `/myroot/proc`.
    5. Changes the root directory to `/myroot/` to simulate a containerized environment.
    6. Launches a BusyBox shell as the init process in the new environment.

    Raises
    ------
    OSError
        If any of the system calls fail, an OSError may be raised.
    """
    create_control_group()
    unshare(flags.CLONE_NEWNS | flags.CLONE_NEWUTS)
    set_hostname("my-container")
    os.system("mount -t proc none /myroot/proc")
    os.chroot("/myroot/")
    os.chdir("/")
    os.execvp("/bin/busybox", ["/bin/busybox", "sh"])


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
    child_func_type = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
    child_func_c = child_func_type(run_child_proc)

    stack = ctypes.c_void_p(libc.sbrk(0))

    pid = libc.clone(
        child_func_c,
        stack,
        flags.CLONE_NEWNS | flags.CLONE_NEWPID,
        flags.CLONE_NEWUTS | flags.CLONE_NEWCGROUP | 17,
    )
    rid, status = os.waitpid(pid, 0)
    print(rid, status)


if __name__ == "__main__":
    run()
