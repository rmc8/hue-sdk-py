from typing import Union, Optional, Any

from .util import _id_check


class Schedules:
    def __init__(self, parent):
        self.base: str = parent.base
        self.request = parent.request
    
    def create_schedule(self, command: dict, time_: str, localtime: str,
                        params: Optional[dict] = None, **kwargs: Any) -> Union[list, dict]:
        payload: dict = {
            "command": command,
            "time": time_,
            "localtime": localtime,
        }
        if type(params) is dict:
            payload.update(params)
        payload.update(kwargs)
        return self.request(path="schedules", method="POST", payload=payload)
    
    def get_attributes(self, id_: Union[int, str]) -> Union[list, dict]:
        _id_check(id_)
        return self.request(path=f"schedules/{id_}")
    
    def set_attributes(self, id_: Union[int, str], params: Optional[dict] = None, **kwargs: Any) -> Union[list, dict]:
        _id_check(id_)
        payload: dict = {}
        if type(params) is dict:
            payload.update(params)
        payload.update(kwargs)
        return self.request(path=f"schedules/{id_}", method="PUT", payload=payload)
    
    def delete(self, id_: Union[int, str]) -> Union[list, dict]:
        return self.request(path=f"schedules/{id_}", method="DELETE")
