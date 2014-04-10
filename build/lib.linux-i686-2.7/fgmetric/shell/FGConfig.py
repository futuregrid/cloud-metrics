import os
import yaml

class FGConfig:
    default_cfg = os.getenv("HOME") + "/.futuregrid/" 
    default_yaml = "futuregrid.yaml"
    default_yaml_path = default_cfg + default_yaml

    def __init__(self):
        self.yaml_path = self.default_yaml_path

    def get_config(self, section=None):
        f = open(self.yaml_path)
        dataMap = yaml.safe_load(f)
        f.close()
        try:
            dataMap = dataMap[section]
        except:
            dataMap = dataMap
        return dataMap

    def set_config(self, dataMap):
        f = open(self.yaml_path, "w")
        yaml.deump(dataMap, f)
        f.close()

    def set_yaml_path(self, path):
        self.yaml_path = path

    def get_yaml_path(self):
        return self.yaml_path
