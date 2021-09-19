class IpAddressFmtException(Exception):
    msg: str = "The format of the IP address is incorrect."


class DeviceTypeException(Exception):
    msg: str = "Invalid devicetype"


class ButtonNotPressedException(Exception):
    msg: str = "Link button was not pressed"


class NoConnectionSettingsException(Exception):
    msg: str = "\n".join([
        "The connection to the Hue Bridge has not been set up.",
        "Use the `hueconn -i={ip_address}` command to connect to the Hue Bridge, please.",
    ])


class CouldNotAuthenticate(Exception):
    msg: str = "Repeated errors occurred during Request with Hue Bridge."
