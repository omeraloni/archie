import click

from .helpers import validate_ip, abort_if_false
from .methods import config_read, config_write, archie_test_login, config_check_password


@click.group(name='config')
def config():
    """Configure router login details"""
    pass


@click.command(name='set')
@click.option('--host', hidden=True, default='192.168.0.1', envvar='ARCHIE_HOSTNAME',
              prompt='Router\'s IP address', callback=validate_ip, show_default=True)
@click.option('--username', hidden=True, default='admin', envvar='ARCHIE_USERNAME',
              prompt='Router\'s admin user name', show_default=True)
@click.option('--password', hidden=True, default='admin', envvar='ARCHIE_PASSWORD',
              prompt='Router\'s admin user password', show_default=True, hide_input=True, confirmation_prompt=True)
@click.option('--save', is_flag=True, default=True, hidden=True, prompt='Save', callback=abort_if_false)
def config_set(host, username, password, save):
    """Set router login details"""
    config_write(host, username, password)


@click.command(name='show')
def config_show():
    """Show router login details"""

    try:
        print(config_read())
    except Exception as e:
        print(e)


@click.command(name='test', hidden=True)
@click.pass_context
def config_test(ctx):
    """Test router login details"""

    archie_test_login(ctx.obj['debug'])


@click.command(name='check')
@click.option('--password', hidden=True,
              prompt='What is your admin user password', hide_input=True)
def config_check(password):
    """Check router password validity"""

    print('Your password is correct' if config_check_password(password) else 'your password is incorrect')


config.add_command(config_set)
config.add_command(config_show)
config.add_command(config_test)
config.add_command(config_check)


