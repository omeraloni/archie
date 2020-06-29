from archie import Archie
import os
import argparse
import schedule
import time
import logging
import platform
import re


global host, username, password, archie, logger, ping_host, ping_failed


def reboot_router_job():
    try:
        archie.login()
        archie.reboot()
        logger.info("Router is rebooting...")
        time.sleep(30) # Archer C7 reboot is ~20 seconds
    except Exception as err:
        logger.error(err)


def ping(hostname, retries=1):
    output = os.popen(' '.join(("ping", f"-c {retries}", hostname))).read()
    result = re.search(r'ttl=([0-9]+) time=([0-9.]+)', output)

    if not result:
        logger.debug(output)
        raise Exception("ping failed")

    return result.group(1), result.group(2)  # ttl, time


def ping_google_job():
    global ping_failed

    try:
        result = ping(ping_host)
        logger.info(f"ping {ping_host} ttl={result[0]} time={result[1]} ms")
    except Exception as err:
        logger.error(err)
        ping_failed = ping_failed + 1

    '''
    if ping_failed > 3:
        reboot_router_job()
        ping_failed = 0
    '''


def setup_logging():
    global logger
    logger = logging.getLogger('archie-cli')
    logger.setLevel(logging.DEBUG)

    console_logger = logging.StreamHandler()
    console_logger.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    console_logger.setLevel(logging.DEBUG)
    logger.addHandler(console_logger)

    file_logger = logging.FileHandler('archie.log')
    file_logger.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    file_logger.setLevel(logging.DEBUG)
    logger.addHandler(file_logger)


def main():

    global host, username, password, archie, ping_host, ping_failed

    # Try to get configuration from environment variables
    host = os.getenv('ARCHIE_HOST', default='192.168.0.1')
    username = os.getenv('ARCHIE_USERNAME', default='admin')
    password = os.getenv('ARCHIE_PASSWORD', default='admin')

    ping_host = "google.com"
    ping_failed = 0

    setup_logging()
    archie = Archie(host, username, password, test_mode=True)

    schedule.every().day.at("23:31").do(reboot_router_job)
    schedule.every(5).seconds.do(ping_google_job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
