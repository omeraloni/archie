import re
from click import BadParameter


def validate_ip(ctx, param, value):
    try:
        result = re.fullmatch(r'([0-9]+).([0-9]+).([0-9]+).([0-9]+)', value)

        if result is None:
            raise ValueError

        return value
    except ValueError:
        raise BadParameter('IP needs to be in the form of xxx.xxx.xxx.xxx')


def validate_time(ctx, param, value):
    try:
        result = re.fullmatch(r'(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])', value)

        if result is None:
            raise ValueError

        return value
    except ValueError:
        raise BadParameter('Time needs to be in the form of HH:MM')