import subprocess
from re import search


def ping(hostname, retries=1):

    command = ["ping", f"-c {retries}", hostname]
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

