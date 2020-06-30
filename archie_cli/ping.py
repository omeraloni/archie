from os import popen
from re import search
import logging


def ping(hostname, retries=1):
    output = popen(' '.join(("ping", f"-c {retries}", hostname))).read()
    result = search(r'ttl=([0-9]+) time=([0-9.]+)', output)

    if not result:
        logger = logging.getLogger('archie-cli')
        logger.error(output)
        raise Exception("ping failed")

    return int(result.group(1)), float(result.group(2))  # ttl, time
