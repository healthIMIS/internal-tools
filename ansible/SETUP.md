# Setup
## SSH
Put the following snippet in your `.ssh/config` and adjust it.

```text
HOST example.org # adjust to domain
    Hostname example.org  # the hostname of the machine running the setup
    User john.doe   # your first.last name
    ControlMaster auto
    ControlPath ~/.ssh/cm-%r@%h:%p
    ControlPersist 5m
    IdentifyFile ~/.ssh/my_key

Host 10.10.10.*
    ProxyCommand ssh -W %h:%p example.org # tunnel through the host defined above

```
with this config, you can easily connect to the host machine running the setup with `ssh example.org` and to any
service running on this host by e.g., `ssh 10.10.10.2`.

**Important:** If the SSH connection does stop working at any point in time and the host become
unreachable, please remove the control socket (i.e., `~/.ssh/cm-%r@%h:%p`) and try again. 