from typing import Union

from colormath.color_conversions import convert_color
from colormath.color_objects import XYZColor, sRGBColor

from .util import range_check, cc_reg
from .exceptions import (
    IdFormatException,
    BrightnessRangeException,
    HueRangeException,
    SaturationRangeException,
    GettingLightAttributeException,
    ColorcodeRangeException,
    NoIuminanceException,
)


class Lights:
    def __init__(self, parent):
        self.base: str = parent.base
        self.request = parent.request
    
    @staticmethod
    def _id_check(light_id: Union[int, str]) -> None:
        if type(light_id) is str and not light_id.isnumeric():
            raise IdFormatException
    
    def get_new_lights(self) -> Union[list, dict]:
        return self.request(path="lights/new")
    
    def search_new_lights(self, payload: dict) -> Union[list, dict]:
        return self.request(path="lights", method="POST", payload=payload)
    
    def get_light_attributes(self, light_id: Union[int, str]) -> Union[list, dict]:
        self._id_check(light_id)
        return self.request(path=f"lights/{light_id}")
    
    def rename(self, light_id: Union[int, str], light_name: str) -> Union[list, dict]:
        self._id_check(light_id)
        return self.request(path=f"lights/{light_id}", method="PUT", payload={"name": light_name})
    
    def set_light_state(self, light_id: Union[int, str], payload: dict) -> Union[list, dict]:
        self._id_check(light_id)
        return self.request(path=f"lights/{light_id}/state",
                            method="PUT",
                            payload=payload)
    
    def on(self, light_id: Union[int, str], transitiontime: int = 5) -> Union[list, dict]:
        return self.set_light_state(light_id, payload={"on": True, "transitiontime": transitiontime})
    
    def off(self, light_id: Union[int, str], transitiontime: int = 5) -> Union[list, dict]:
        return self.set_light_state(light_id, payload={"on": False, "transitiontime": transitiontime})
    
    def toggle(self, light_id: Union[int, str], transitiontime: int = 5) -> Union[list, dict]:
        res: dict = self.get_light_attributes(light_id=light_id)
        if right := res.get("state"):
            if right.get("on"):
                return self.off(light_id, transitiontime)
            return self.on(light_id, transitiontime)
        raise GettingLightAttributeException
    
    @range_check(name="bri", start=1, end=254, exception=BrightnessRangeException)
    def brightness(self, light_id: Union[int, str], val: int) -> Union[list, dict]:
        return self.set_light_state(light_id, payload={"bri": val})
    
    @range_check(name="hue", start=0, end=65535, exception=HueRangeException)
    def hue(self, light_id: Union[int, str], val: int) -> Union[list, dict]:
        return self.set_light_state(light_id, payload={"hue": val})
    
    @range_check(name="sat", start=0, end=254, exception=SaturationRangeException)
    def saturation(self, light_id: Union[int, str], val: int) -> Union[list, dict]:
        return self.set_light_state(light_id, payload={"sat": val})
    
    def xy(self, light_id: Union[int, str],
           x: float, y: float, transitiontime: int = 5) -> Union[list, dict]:
        return self.set_light_state(
            light_id=light_id,
            payload={
                "xy": [x, y],
                "transitiontime": transitiontime,
            },
        )
    
    def alert(self, light_id: Union[int, str], alert_type: str = "select") -> Union[list, dict]:
        return self.set_light_state(light_id, payload={"alert": alert_type})
    
    def effect(self, light_id: Union[int, str], mode: str = "colorloop") -> Union[list, dict]:
        return self.set_light_state(light_id, payload={"effect": mode})
    
    @staticmethod
    def cc_range(num: Union[int, float]) -> Union[list, dict]:
        return not 255 >= num >= 0
    
    def rgb(self, light_id: Union[int, str], r: int, g: int, b: int, transitiontime: int = 5) -> Union[list, dict]:
        if self.cc_range(r) or self.cc_range(g) or self.cc_range(b):
            raise ColorcodeRangeException
        elif not all((r, g, b)):
            raise NoIuminanceException
        red: float = r / 255
        green: float = g / 255
        blue: float = b / 255
        rgb = sRGBColor(red, green, blue)
        xyz = convert_color(rgb, XYZColor, target_illuminant="d50")
        xyz_sum: float = (xyz.xyz_x + xyz.xyz_y + xyz.xyz_z)
        x: float = xyz.xyz_x / xyz_sum
        y: float = xyz.xyz_y / xyz_sum
        return self.xy(light_id, x, y, transitiontime=transitiontime)
    
    def rgbhex(self, light_id: Union[int, str], color_code: str, transitiontime: int = 5) -> Union[list, dict]:
        cc_reg(color_code)
        cnv: int = 1 if len(color_code) == 7 else 2
        c: str = color_code[1:]
        rgb: dict = {k: int(c[int(n * 2 / cnv):int((n + 1) * 2 / cnv)], 16) for n, k in enumerate("rgb")}
        print(rgb)
        return self.rgb(light_id, **rgb, transitiontime=transitiontime)
    
    def delete(self, light_id: Union[int, str]) -> Union[list, dict]:
        self.request(path=f"lights/{light_id}", method="DELETE")
