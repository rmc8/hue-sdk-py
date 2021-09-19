import logging
from typing import Optional, Union

import requests
from pandas import DataFrame
from pandas.io.json import json_normalize

from . import util
from .all import All
from .lights import Lights
from .exceptions import (
    NoConnectionSettingsException,
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
        self.all = All(self)
        self.lights = Lights(self)
    
    def request(self, path: str = "", method: str = "GET",
                user_name: Optional[str] = None,
                payload: Optional[dict] = None) -> Union[list, dict]:
        user_name: str = user_name if user_name else self.user_name
        base = self.base.format(user_name=user_name)
        endpoint: str = f"{base}/{path}"
        
        res = requests.request(method=method, url=endpoint, json=payload).json()
        
        # Log
        print(f"{method}: {endpoint}")
        logger.debug("=-" * 32)
        logger.debug(f"{method}: {endpoint}")
        logger.debug(res)
        return res
    
    @staticmethod
    def to_dataframe(res: dict, id_exists=False) -> DataFrame:
        if id_exists:
            table = []
            for key, value in res.items():
                value["id"] = key
                table.append(value)
            df = json_normalize(table, max_level=5)
            columns = [col for col in df.columns.tolist() if col != "id"]
            return df[["id"] + columns[:-1]]
        return json_normalize(list(res.values()), max_level=5)
