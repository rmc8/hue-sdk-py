import logging

import requests
from retry import retry

from . import util
from .exceptions import (
    NoConnectionSettingsException,
    CouldNotAuthenticate,
)

logging.basicConfig(filename="hue.log", level=logging.DEBUG)
logger = logging.getLogger("hue")


class Hue:
    
    def __init__(self):
        yc = util.YamlConfig()
        if not yc.exists():
            raise NoConnectionSettingsException
        settings: dict = yc.load()
        self.ip: str = settings["Auth"]["ip"]
        self.user_name: str = settings["Auth"]["user_name"]
        self.base: str = f"http://{self.ip}/api/{self.user_name}"
    
    @retry(
        delay=util.AUTH_FAILURE_SLEEP,
        tries=util.AUTH_FAILURE_RETRIES,
        exceptions=CouldNotAuthenticate,
    )
    def request(self, path: str = "", method: str = "GET", payload=None):
        endpoint: str = f"{self.base}/{path}"
        res = requests.request(method=method, url=endpoint, data=payload).json()[0]
        
        # Log
        logger.debug("=-" * 32)
        logger.debug(f"{method}: {endpoint}")
        logger.debug(res)
        
        # Inspect Request
        if res.get("error"):
            raise CouldNotAuthenticate
        return res
