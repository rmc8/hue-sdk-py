from typing import Union, Optional, Any

from .util import _id_check


class Scenes:
    def __init__(self, parent):
        self.base: str = parent.base
        self.request = parent.request
    
    def create(self, name: str, recycle: bool, type_: str,
               group: Optional[Union[int, str]] = None, lights: list = None,
               params: Optional[dict] = None, **kwargs: Any) -> Union[list, dict]:
        payload: dict = {
            "name": name,
            "recycle": recycle,
            "type": type_,
        }
        if group is not None:
            _id_check(group)
            payload["group"] = group
        elif lights is not None:
            payload["lights"] = lights
        if params is not None:
            payload.update(params)
        payload.update(kwargs)
        return self.request(path="scenes", method="POST", payload=payload)

    def modify(self):
        pass
    
    def delete(self):
        pass
        # return self.request(path=f"schedules/{id_}", method="DELETE")

    def get(self):
        pass