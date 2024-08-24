
Finds errors in a log file and processes them using an external API, Ollama.

The `find_errors_in_log_file()` function reads a log file specified as a command-line argument,
searches for lines containing error-related keywords, and extracts the surrounding context
(a configurable number of lines before and after the error line). The extracted error logs
are returned as a list.

The `process_error_logs()` function takes the list of error logs and sends them to an external
API for further processing. The API response is then printed to the console.



## Ollama setup 

### Ollama setup instructions: https://ollama.com/download

Download model with:
```
ollama pull pki/logpt
```

It's (for now ) a low footprint code, should only need the below to run.
```
pip install requests json
```



## Example run #1 and output

```python3.11 analyzer.py auth.log ```

These logs show that there are multiple failed login attempts to the SSH server on your system. The attacker is trying different usernames and passwords, but they all fail due to PAM (Pluggable Authentication Modules) authentication errors. 

The attacker is coming from IP address `10.1.30.35`, which seems to be a private IP address within your local network. You should investigate this IP address to see if it's a legitimate user or an unauthorized device on your network. If it's an unauthorized device, you should take steps to remove it from your network.

## Example run #2 and output
```
python3.11 analyzer.py  proxmox.log
```
The log messages you provided are related to Proxmox Virtual Environment (PVE), a popular open-source platform for managing virtual machines and containers. Here's a brief explanation of each message:

1. "VM quit/powerdown failed - terminating now with SIGTERM": This error indicates that the system was unable to gracefully shut down a virtual machine (VM) using the SIGTERM signal, which is usually sent to request a clean exit. It then forcefully terminated the VM using the SIGKILL signal.

2. "VM still running - terminating now with SIGKILL": This error occurs when the system was unable to stop a VM using SIGTERM and had to resort to using SIGKILL, which forcibly kills the process without allowing it to clean up.

3. "error rbd: sysfs write failed": This is an error related to Ceph, a distributed storage system used by PVE. It indicates that there was a problem writing data to the sysfs interface, which is used for communication between kernel modules and user-space processes.

4. "can't unmap rbd device /dev/rbd-pve/e1b44232-4460-4fcc-b30d-dbcb4fdad215/ceph/vm-54412-disk-0: rbd: sysfs write failed": This error is similar to the previous one, but it occurs when trying to unmap a block device used by Ceph.

5. "volume deactivation failed: ceph:vm-54412-disk-0 at /usr/share/perl5/PVE/Storage.pm line 1264": This error indicates that there was an issue deactivating a storage volume (likely related to Ceph) in PVE, which could be due to the previous errors with sysfs write failures.

6. "Error: root@host /etc/pve/firewall #FTG": This is not an error message but rather a prompt indicating that you are logged in as the root user on a machine named host and you are in the /etc/pve/firewall directory. The "#" symbol indicates that you have superuser privileges, and "FTG" is likely a command or part of a command that was intended to be executed but not completed.

In summary, these messages indicate issues with VM management and storage related to Ceph in PVE. An experienced user would need more context and information about the system configuration and state to diagnose the root cause of these errors and suggest possible solutions.


