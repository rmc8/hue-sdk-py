import re
import argparse

import requests
from retry import retry

from . import util
from .exceptions import (
    DeviceTypeException,
    ButtonNotPressedException,
)





def get_args():
    parser = argparse.ArgumentParser(
        description="Make a request to the specified endpoint and attempt to connect Python to the Hue Bridge"
    )
    parser.add_argument("-i", "--ip", type=str, required=True, help="IP address of Hue Bridge")
    parser.add_argument("-d", "--domain", type=bool,
                        required=False, default=True,
                        help="If you want to specify a domain instead of an IP, set this argument to False")
    return parser.parse_args()


@retry(
    delay=util.AUTH_FAILURE_SLEEP,
    tries=util.AUTH_FAILURE_RETRIES,
    exceptions=ButtonNotPressedException,
)
def main():
    # Get an IP address.
    args = get_args()
    ip: str = args.ip
    if args.domain:
        util.ip_reg(ip)
    
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
