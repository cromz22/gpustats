#!/usr/bin/env/python3

# Usage: python3 gpustats.py
# Please read README.md for more details.

from multiprocessing import Process
import paramiko


class Color:
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    END       = '\033[0m'


def get_gpu_stat(host, host_ncards):
    username = "your-user-name"
    ssh_private_key = f"/home/{username}/.ssh/id_ed25519"
    known_hosts = f"/home/{username}/.ssh/known_hosts"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.load_host_keys(known_hosts)

    client.connect(host, username=username, key_filename=ssh_private_key)

    # get_gpus="nvidia-smi --query-gpu=gpu_uuid --format=csv,noheader"
    get_used_gpus = "nvidia-smi --query-compute-apps=gpu_uuid --format=csv,noheader"

    stdin, stdout, stderr = client.exec_command(get_used_gpus)

    used_gpus = []
    for line in stdout:
        strip = line.strip()
        if strip != "":
            used_gpus.append(strip)

    n_used = len(used_gpus)
    n_cards = host_ncards[host]

    string = f"{host:8s}: {n_used:2d} / {n_cards:2d} GPU cards are used"

    if n_used == 0:
        string = Color.GREEN + string + Color.END
    elif n_used == n_cards:
        string = Color.RED + string + Color.END
    else:
        string = Color.YELLOW + string + Color.END

    print(string)

    client.close()
    del client, stdin, stdout, stderr


def main():
    host_ncards = {
        "host1": 8,  # "hostname": the number of GPU cards of the host,
        "host2": 4,
        "host3": 4,
    }

    process_list = []
    for host in host_ncards.keys():
        process = Process(target=get_gpu_stat, args=(host, host_ncards))
        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()


if __name__ == "__main__":
    main()
