import json
import os
import logging

from archie import Archie


def archie_reboot():
    logger = logging.getLogger('archie-cli')
    cfg = config_read()

    archie = Archie(host=cfg["host"],
                    username=cfg["username"],
                    password=cfg["password"])

    archie.login()
    # archie.reboot()
    logger.warning("Router is rebooting")


def config_write(host, username, password):
    location = f"{os.environ.get('HOME')}/.config/archie"

    if os.path.exists(location) is False:
        os.mkdir(location)

    os.chdir(location)

    config_file = f"{location}/config.json"

    with open(config_file, 'w') as file:
        cfg = {
            'host': host,
            'username': username,
            'password': password
        }

        json.dump(cfg, file)
        print('Saved!')


def config_read():
    config_file = f"{os.environ.get('HOME')}/.config/archie/config.json"

    if os.path.isfile(config_file) is False:
        raise FileNotFoundError("Configuration file not found")

    with open(config_file, 'r') as file:
        return json.load(file)