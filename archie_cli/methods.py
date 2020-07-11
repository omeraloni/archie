import json
import os
import logging

from .archie import Archie
from .cli import debug_mode


def archie_reboot():

    cfg = config_read()

    archie = Archie(host=cfg["host"], username=cfg["username"], password=cfg["password"], debug_mode=debug_mode)
    archie.login()
    archie.reboot()
    logging.getLogger('archie-cli').warning("Router is rebooting")


def archie_test_login():

    cfg = config_read()

    archie = Archie(host=cfg["host"], username=cfg["username"], password=cfg["password"], debug_mode=debug_mode)
    archie.login()
    logging.getLogger('archie-cli').info(f"Logged-in, token is {archie.token}")


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