# Simple Linux Container Runtime

This project is a simple Linux container runtime that creates isolated child processes using Linux namespaces and control groups (cgroups). It demonstrates how to create a minimal container environment by setting up a jail filesystem, isolating the process with namespaces, and managing resource limits using cgroups.

## Features

- **Namespace Isolation**: The runtime isolates the process using Linux namespaces (`CLONE_NEWNS`, `CLONE_NEWUTS`, `CLONE_NEWPID`), providing separate environments for the mount, UTS (hostname), and process ID namespaces.
- **Filesystem Jail**: The child process is placed in a restricted, jailed filesystem (`chroot`) to simulate a container environment.
- **Control Groups (cgroups)**: The runtime uses cgroups to limit and manage resources like memory for the child process.
- **BusyBox Shell**: The runtime launches a BusyBox shell as the init process inside the container.

## Prerequisites

- **Linux Kernel**: The runtime requires a Linux kernel with support for namespaces and cgroups.
- **BusyBox**: A BusyBox executable must be available in the system to serve as the shell inside the container.
