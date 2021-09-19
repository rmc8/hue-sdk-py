import re
import argparse

import requests
from retry import retry

from . import util
from .exceptions import (
    IpAddressFmtException,
    DeviceTypeException,
    ButtonNotPressedException,
)


def ip_reg(ip_address_str: str):
    ptn = re.compile(
        r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    )
    if not ptn.match(ip_address_str):
        raise IpAddressFmtException


def get_args():
    parser = argparse.ArgumentParser(description="Enter the region and bucket name and the path of the file to split for uploading to S3.")
    parser.add_argument("-i", "--ip", type=str, required=True, help="IP address of Hue Bridge")
    return parser.parse_args()


@retry(
    exceptions=ButtonNotPressedException,
    tries=3,
    delay=10,
)
def main():
    # Get an IP address.
    args = get_args()
    ip: str = args.ip
    ip_reg(ip)
    
    # Attempt to authenticate with Hue Bridge
    payload: dict = {"devicetype": "hue_cli"}
    url: str = f"http://{ip}/api"
    res: dict = requests.post(url, json=payload).json()[0]
    
    # Error handling
    if error := res.get("error"):
        if error["type"] == 1:
            raise DeviceTypeException
        print(ButtonNotPressedException.msg)
        raise ButtonNotPressedException
    
    # Exporting authentication information
    user_name = res["success"]["username"]
    settings: dict = {
        "Auth": {
            "ip": ip,
            "user_name": user_name
        }
    }
    yc = util.YamlConfig()
    yc.write(settings)
    
    # Output for console
    print("The authentication information has been registered as follows.")
    print(settings)
    print()


if __name__ == "__main__":
    main()
