import os

import yaml

AUTH_FAILURE_RETRIES: int = 6
AUTH_FAILURE_SLEEP: int = 5


class YamlConfig:
    cur_path: str = os.path.dirname(os.path.abspath(__file__))
    
    def __init__(self, file_path: str = f"{cur_path}/config.yml"):
        self.file_path = file_path
    
    def exists(self):
        return os.path.exists(self.file_path)
    
    def load(self) -> dict:
        """
        :return: Return yaml data as dictionary format
        """
        with open(self.file_path, "r", encoding="utf-8") as yf:
            return yaml.load(yf, Loader=yaml.FullLoader)
    
    def write(self, data: dict) -> None:
        """
        Export yaml
        :param data: A dictionary of data that will be output in Yaml format
        """
        with open(self.file_path, "w", encoding="utf-8") as yf:
            yaml.dump(data, yf, default_flow_style=False)
