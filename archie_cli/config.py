import json
import os
import click
from .helpers import validate_ip, abort_if_false


@click.group(name='config')
def config():
    """Configure router login details"""
    pass


@click.command(name='set')
@click.option('--host', hidden=True, default='192.168.0.1', envvar='ARCHIE_HOSTNAME', help='Router\'s IP address',
              prompt='Router\'s IP address', callback=validate_ip, show_default=True)
@click.option('--username', hidden=True, default='admin', envvar='ARCHIE_USERNAME', help='Router\'s admin user name',
              prompt='Router\'s admin user name', show_default=True)
@click.option('--password', hidden=True, default='admin', envvar='ARCHIE_PASSWORD',
              help='Router\'s admin user password',
              prompt='Router\'s admin user password', show_default=True, hide_input=True, confirmation_prompt=True)
@click.option('--save', is_flag=True, default=True, hidden=True, prompt='Save', callback=abort_if_false)
def config_set(host, username, password, save):
    """Set router login details"""

    location = os.environ.get('HOME', '') + '/.config/archie'

    if os.path.exists(location) is False:
        os.mkdir(location)

    os.chdir(location)
    with open('config.json', 'w') as file:
        cfg = {
            'host': host,
            'username': username,
            'password': password
        }

        json.dump(cfg, file)
        print('Saved!')


@click.command(name='show')
@click.pass_context
def config_show(ctx):
    """Set router login details"""

    location = os.environ.get('HOME', '') + '/.config/archie'
    if os.path.exists(location) is False:
        print('No configuration saved')
        ctx.abort()

    os.chdir(location)

    if os.path.isfile('config.json') is False:
        print('No configuration saved')
        ctx.abort()

    with open('config.json', 'r') as file:
        cfg = json.load(file)
        print(cfg)


config.add_command(config_set)
config.add_command(config_show)
