from typing import Union

from .util import range_check, _id_check, rgb2xy, hex2dec
from .exceptions import (
    BrightnessRangeException,
    HueRangeException,
    SaturationRangeException,
    GettingLightAttributeException,
)


class Lights:
    def __init__(self, parent):
        self.base: str = parent.base
        self.request = parent.request
    
    def get_new_lights(self) -> Union[list, dict]:
        return self.request(path="lights/new")
    
    def search_new_lights(self, payload: dict) -> Union[list, dict]:
        return self.request(path="lights", method="POST", payload=payload)
    
    def get_attributes(self, light_id: Union[int, str]) -> Union[list, dict]:
        _id_check(light_id)
        return self.request(path=f"lights/{light_id}")
    
    def rename(self, light_id: Union[int, str], light_name: str) -> Union[list, dict]:
        _id_check(light_id)
        return self.request(path=f"lights/{light_id}", method="PUT", payload={"name": light_name})
    
    def action(self, light_id: Union[int, str], payload: dict) -> Union[list, dict]:
        _id_check(light_id)
        return self.request(path=f"lights/{light_id}/state",
                            method="PUT",
                            payload=payload)
    
    def on(self, light_id: Union[int, str], transitiontime: int = 5) -> Union[list, dict]:
        return self.action(light_id, payload={"on": True, "transitiontime": transitiontime})
    
    def off(self, light_id: Union[int, str], transitiontime: int = 5) -> Union[list, dict]:
        return self.action(light_id, payload={"on": False, "transitiontime": transitiontime})
    
    def toggle(self, light_id: Union[int, str], transitiontime: int = 5) -> Union[list, dict]:
        res: dict = self.get_attributes(light_id=light_id)
        if right := res.get("state"):
            if right.get("on"):
                return self.off(light_id, transitiontime)
            return self.on(light_id, transitiontime)
        raise GettingLightAttributeException
    
    @range_check(name="bri", start=1, end=254, exception=BrightnessRangeException)
    def brightness(self, light_id: Union[int, str], val: int) -> Union[list, dict]:
        return self.action(light_id, payload={"bri": val})
    
    @range_check(name="hue", start=0, end=65535, exception=HueRangeException)
    def hue(self, light_id: Union[int, str], val: int) -> Union[list, dict]:
        return self.action(light_id, payload={"hue": val})
    
    @range_check(name="sat", start=0, end=254, exception=SaturationRangeException)
    def saturation(self, light_id: Union[int, str], val: int) -> Union[list, dict]:
        return self.action(light_id, payload={"sat": val})
    
    def alert(self, light_id: Union[int, str], alert_type: str = "select") -> Union[list, dict]:
        return self.action(light_id, payload={"alert": alert_type})
    
    def effect(self, light_id: Union[int, str], mode: str = "colorloop") -> Union[list, dict]:
        return self.action(light_id, payload={"effect": mode})
    
    def xy(self, light_id: Union[int, str],
           x: float, y: float, transitiontime: int = 5) -> Union[list, dict]:
        return self.action(
            light_id=light_id,
            payload={
                "xy": [x, y],
                "transitiontime": transitiontime,
            },
        )
    
    def rgb(self, light_id: Union[int, str], r: int, g: int, b: int, transitiontime: int = 5) -> Union[list, dict]:
        x, y = rgb2xy(r, g, b)
        return self.xy(light_id, x, y, transitiontime=transitiontime)
    
    def rgbhex(self, light_id: Union[int, str], color_code: str, transitiontime: int = 5) -> Union[list, dict]:
        rgb: dict = hex2dec(color_code)
        return self.rgb(light_id, **rgb, transitiontime=transitiontime)
    
    def delete(self, light_id: Union[int, str]) -> Union[list, dict]:
        return self.request(path=f"lights/{light_id}", method="DELETE")
