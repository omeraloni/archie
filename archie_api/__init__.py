import requests
import requests.compat
import hashlib
import base64
import re
import logging


class ArchieAPI:
    def __init__(self, host, username, password, debug_log=False):
        """Initialize the scanner."""
        self.credentials = ''
        self.token = ''
        self.host = host
        self.username = username
        self.password = password

        # Set up logging
        self._logger = logging.getLogger('archie_api')

        if debug_log:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.ERROR)

        console_logger = logging.StreamHandler()
        console_logger.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self._logger.addHandler(console_logger)

        self._logger.info("Initialized ArchieAPI")

    def _get_response(self, url, timeout=4):
        referer = f"http://{self.host}"
        cookie = {"Authorization": f"Basic{self.credentials}"}

        return requests.get(url, cookies=cookie,
                            headers={'Referer': referer}, timeout=timeout)

    def _get_auth_token(self):
        self._logger.info("Retrieving authentication token from router")

        '''
        There seems to be some sort of state machine maintained on the
        router that needs a request here first.
        '''
        requests.get(f"http://{self.host}")

        '''
        Generate md5 hash of password. 
        The C7 appears to use the first 15 characters of the password only, 
        so we truncate to remove additional characters from being hashed.
        '''
        password = hashlib.md5(self.password.encode('utf')).hexdigest()
        credentials = f"{self.username}:{password}".encode('utf')

        '''
        Encode credentials to be sent as a cookie
        '''
        credentials = base64.b64encode(credentials).decode('utf')
        credentials = requests.compat.quote(' ' + credentials)
        self.credentials = credentials

        try:
            response = self._get_response(f"http://{self.host}/userRpm/LoginRpm.htm?Save=Save")

            result = re.search(r'window.parent.location.href = '
                               r'"https?://.*/(.*)/userRpm/Index.htm";',
                               response.text)

            if not result:
                self._logger.error(f"Unable to fetch auth token for {self.host}")
                self._logger.debug(f"Response: {response.content}")
                raise Exception("Unexpected response")

            self.token = result.group(1)
            self._logger.info(f"Your token is {self.token}")

        except ValueError:
            self._logger.error(f"Unable to fetch auth token for {self.host}")
            raise ValueError("Unexpected value")

    def login(self):
        self._get_auth_token()
        self._logger.info(f"Logged in to http://{self.host} as {self.username}")

    def get_info(self):
        return self._get_response(f"http://{self.host}/{self.token}/userRpm/WanCfgRpm.html")

    def reboot(self):
        self._logger.info("Rebooting router")
        return self._get_response(f"http://{self.host}/{self.token}/userRpm/SysRebootRpm.htm?Reboot=Reboot")

