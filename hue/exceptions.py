class IpAddressFmtException(Exception):
    msg: str = "The format of the IP address is incorrect."


class DeviceTypeException(Exception):
    msg: str = "Invalid devicetype."


class ButtonNotPressedException(Exception):
    msg: str = "Link button was not pressed."


class NoConnectionSettingsException(Exception):
    msg: str = "\n".join([
        "The connection to the Hue Bridge has not been set up.",
        "Use the `hueconn -i={ip_address}` command to connect to the Hue Bridge, please.",
    ])


class CouldNotAuthenticate(Exception):
    msg: str = "Repeated errors occurred during Request with Hue Bridge."


class IdFormatException(Exception):
    msg: str = "Invalid format, ID must be of type Int or String with integer value."


class BrightnessRangeException(Exception):
    pass


class HueRangeException(Exception):
    pass


class SaturationRangeException(Exception):
    pass


class GettingLightAttributeException(Exception):
    msg: str = "Failed to get the Light attribute"


class ColorcodeFormatException(Exception):
    msg: str = "Color code format error. Please set as follows.\nFormat: ^#[A-Fa-f0-9]{6}$"


class ColorcodeRangeException(Exception):
    msg: str = "The value of each channel should be set to an integer value between 0 and 255."


class NoIuminanceException(Exception):
    msg: str = "There is no brightness because all RGB are 0. " \
               "Set one of the RGBs to an integer value between 1 and 255, please."
