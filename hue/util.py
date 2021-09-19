import os
import re

import yaml
import numpy as np

from .exceptions import ColorcodeFormatException, IpAddressFmtException

AUTH_FAILURE_RETRIES: int = 6
AUTH_FAILURE_SLEEP: int = 5


class YamlConfig:
    cur_path: str = os.path.dirname(os.path.abspath(__file__))
    
    def __init__(self, file_path: str = f"{cur_path}/config.yml"):
        self.file_path = file_path
    
    def exists(self):
        return os.path.exists(self.file_path)
    
    def load(self) -> dict:
        """
        :return: Return yaml data as dictionary format
        """
        with open(self.file_path, "r", encoding="utf-8") as yf:
            return yaml.load(yf, Loader=yaml.FullLoader)
    
    def write(self, data: dict) -> None:
        """
        Export yaml
        :param data: A dictionary of data that will be output in Yaml format
        """
        with open(self.file_path, "w", encoding="utf-8") as yf:
            yaml.dump(data, yf, default_flow_style=False)


def range_check(name, start, end, exception):
    def set_fx(fx):
        def inner(*args, **kwargs):
            num: int = kwargs["val"]
            if type(num) is not int or num > end or num < start:
                raise exception(f"The value of {name} should be an integer value between {start} and {end}.")
            return fx(*args, **kwargs)
        
        return inner
    
    return set_fx


def ip_reg(ip_address_str: str):
    ptn = re.compile(
        r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    )
    if not ptn.match(ip_address_str):
        raise IpAddressFmtException


def cc_reg(color_code: str):
    ptn = re.compile(r"^#[A-Fa-f0-9]{6}$")
    if not ptn.match(color_code):
        raise ColorcodeFormatException
