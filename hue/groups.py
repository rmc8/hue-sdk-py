from typing import Union, List

from .util import range_check, _id_check, rgb2xy, hex2dec
from .exceptions import (
    BrightnessRangeException,
    HueRangeException,
    SaturationRangeException,
)


class Groups:
    def __init__(self, parent):
        self.base: str = parent.base
        self.request = parent.request
    
    def create(self, light_list: List[str], name: str,
                     group_type: str = "LightGroup", cls: str = "other") -> Union[list, dict]:
        return self.request(
            path="groups", method="POST",
            payload={
                "lights": light_list,
                "name": name,
                "type": group_type,
                "class": cls
            }
        )
    
    def get_attributes(self, group_id: Union[str, int]):
        _id_check(group_id)
        return self.request(path=f"groups/{group_id}")
    
    def set_attributes(self, group_id: Union[str, int], payload: dict) -> Union[list, dict]:
        _id_check(group_id)
        return self.request(path=f"groups/{group_id}/",
                            method="PUT",
                            payload=payload)
    
    def rename(self, group_id: Union[str, int],
               name: str, cls: str = "Other") -> Union[list, dict]:
        return self.set_attributes(
            group_id, payload={"name": name, "class": cls}
        )
    
    def set_lights(self, group_id: Union[str, int],
                   light_list: List[str], cls: str = "Other") -> Union[list, dict]:
        return self.set_attributes(
            group_id, payload={"lights": light_list, "class": cls}
        )
    
    def action(self, group_id: Union[int, str], payload: dict) -> Union[list, dict]:
        _id_check(group_id)
        return self.request(path=f"groups/{group_id}/action",
                            method="PUT",
                            payload=payload)
    
    def on(self, group_id: Union[int, str]) -> Union[list, dict]:
        return self.action(group_id, payload={"on": True})
    
    def off(self, group_id: Union[int, str]) -> Union[list, dict]:
        return self.action(group_id, payload={"on": False})
    
    @range_check(name="bri", start=1, end=254, exception=BrightnessRangeException)
    def brightness(self, group_id: Union[int, str], val: int) -> Union[list, dict]:
        return self.action(group_id, payload={"bri": val})
    
    @range_check(name="hue", start=0, end=65535, exception=HueRangeException)
    def hue(self, group_id: Union[int, str], val: int) -> Union[list, dict]:
        return self.action(group_id, payload={"hue": val})
    
    @range_check(name="sat", start=0, end=254, exception=SaturationRangeException)
    def saturation(self, group_id: Union[int, str], val: int) -> Union[list, dict]:
        return self.action(group_id, payload={"sat": val})
    
    def alert(self, group_id: Union[int, str], alert_type: str = "select") -> Union[list, dict]:
        return self.action(group_id, payload={"alert": alert_type})
    
    def effect(self, group_id: Union[int, str], mode: str = "colorloop") -> Union[list, dict]:
        return self.action(group_id, payload={"effect": mode})
    
    def xy(self, group_id: Union[int, str],
           x: float, y: float, transitiontime: int = 5) -> Union[list, dict]:
        return self.action(
            group_id=group_id,
            payload={
                "xy": [x, y],
                "transitiontime": transitiontime,
            },
        )
    
    def rgb(self, group_id: Union[int, str], r: int, g: int, b: int, transitiontime: int = 5) -> Union[list, dict]:
        x, y = rgb2xy(r, g, b)
        return self.xy(group_id, x, y, transitiontime=transitiontime)
    
    def rgbhex(self, group_id: Union[int, str], color_code: str, transitiontime: int = 5) -> Union[list, dict]:
        rgb: dict = hex2dec(color_code)
        return self.rgb(group_id, **rgb, transitiontime=transitiontime)
    
    def scene(self, group_id: Union[int, str], scene: str) -> Union[list, dict]:
        return self.action(group_id, payload={"scene": scene})
    
    def delete(self, group_id: Union[int, str]) -> Union[list, dict]:
        return self.request(path=f"groups/{group_id}", method="DELETE")
