# gpustats
A python script to check the current status of multiple GPU machines.


## Preliminaries

When running tasks using multiple GPU machines, it is hard to remember which ones you are already using and which ones not.
This script enables you to connect asynchronically to multiple GPU machines and get the number of used GPU cards for each machine.

To use this script, you need to have:
- Access to (multiple) GPU machines where the `nvidia-smi` command can be run
- All machines be accessible through the `ssh` command with public key authentication from the client

If you do not have a key pair to connect to the machines, you can create one in the following way:

1. Create an ssh key pair at the client machine
	```
	cd ~/.ssh
	ssh-keygen -t ed25519
	```
1. Copy the created public key to the host machine (e.g. using `rsync`), and add the key to `~/.ssh/authorized_keys`
	```
	cat id_ed25519.pub >> authorized_keys
	```

1. Check the permission of the files inside the `~/.ssh` directory:
	- `.ssh`: 700
	- private key: 600
	- public key: 644
	- `authorized_keys`: 600


## Requirements

- python >= 3.6
- paramiko


## Usage

1. Change the username (and `ssh_private_key`, if necessary) at `gpustats.py` line 11

1. Define the list of hostnames and the number of GPU cards of the host machine at `gpustats.py` line 38 

1. Execute the script
	```
	python3 gpustats.py
	```
