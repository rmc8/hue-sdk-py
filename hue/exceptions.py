class IpAddressFmtException(Exception):
    msg: str = "The format of the IP address is incorrect."


class DeviceTypeException(Exception):
    msg = "Invalid devicetype"


class ButtonNotPressedException(Exception):
    msg = "Link button was not pressed"
