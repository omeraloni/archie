import subprocess
from re import search

from .methods import config_read


def ping(hostname, retries=1):

    ping_cmd = config_read()["ping_cmd"]

    command = [f"{ping_cmd}", f"-c {retries}", hostname]
    output, err = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    output = output.decode('utf-8')
    err = err.decode('utf-8').rstrip('\n')

    if err:
        raise Exception(err)

    try:
        result = search(r'ttl=([0-9]+) time=([0-9.]+)', output)
        return int(result.group(1)), float(result.group(2))  # ttl, time
    except ValueError:
        raise Exception('ping: failed to parse output')

