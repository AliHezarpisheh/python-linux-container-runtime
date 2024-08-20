"""Module containing control group creations and assignments functions."""

import os


def create_control_group() -> None:
    """
    Create and configures a control group for resource management.

    This function creates a custom control group in the `/sys/fs/cgroup/mg` directory
    and assigns the current process to it. It also sets a memory limit for the control
    group.

    Raises
    ------
    OSError
        If there is an issue creating the cgroup or writing to its configuration files.
    """
    dir = "/sys/fs/cgroup/mg"
    # Create the custom cgroup directory if it is not
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Assign current process to the cgroup
    cgroup_processes_dir = os.path.join(dir, "/cgroup.proc")
    with open(cgroup_processes_dir, "w") as file:
        pid = str(os.getpid())
        file.write(pid)

    # Customize the created cgroup
    cgroup_memory_max_file = os.path.join(dir, "/memory.max")
    with open(cgroup_memory_max_file, "w") as file:
        max_bytes = str(512 * 1024 * 1024)
        file.write(max_bytes)
