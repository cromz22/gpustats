#!/usr/bin/env/python3

# Usage: python3 gpustats.py
# Please read README.md for more details.

from multiprocessing import Process
import paramiko


def get_gpu_stat(host, host_ncards):
    username = "your-user-name"
    ssh_private_key = f"/homes/{username}/.ssh/id_ed25519"
    known_hosts = f"/homes/{username}/.ssh/known_hosts"

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
    print(f"{host:8s}: {len(used_gpus):2d} / {host_ncards[host]:2d} GPU cards are used")

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
