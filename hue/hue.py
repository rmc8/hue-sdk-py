import logging
from typing import Optional

import requests
from retry import retry

from . import util
from .all import All
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
        settings: dict = yc.load()["Auth"]
        ip: str = settings["ip"]
        self.user_name: str = settings["user_name"]
        self.base: str = f"http://{ip}/api/{{user_name}}"
        self.get = All(self)
    
    @retry(
        delay=util.AUTH_FAILURE_SLEEP,
        tries=util.AUTH_FAILURE_RETRIES,
        exceptions=CouldNotAuthenticate,
    )
    def request(self, path: str = "", method: str = "GET",
                user_name: Optional[str] = None,
                payload: Optional[dict] = None):
        user_name: str = user_name if user_name else self.user_name
        base = self.base.format(user_name=user_name)
        endpoint: str = f"{base}/{path}"
        
        res = requests.request(method=method, url=endpoint, json=payload).json()
        
        # Log
        logger.debug("=-" * 32)
        logger.debug(f"{method}: {endpoint}")
        logger.debug(res)
        return res
