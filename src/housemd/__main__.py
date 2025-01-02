from .builder import build
from .live import live
from os import path
import json
import sys

def preprocess_configs(configs):
    for k in ["source", "output", "templates"]:
        if k not in configs:
            raise BaseException(f"Config file missing required key `{k}`")

        configs[k] = path.abspath(configs[k])

    configs["mdb"] = None if "mdb" not in configs else path.abspath(configs["mdb"])
    configs["port"] = 0 if "port" not in configs else int(configs["port"])
    configs["trigger_threshold"] = 3 if "trigger_threshold" not in configs else float(configs["trigger_threshold"])

    return configs

def get_configs(configs_path):
    return preprocess_configs(json.load(open(configs_path, "r")))

def get_configs_path():
    if len(sys.argv) != 2:
        raise BaseException("Invalid syntax!")

    return path.abspath(sys.argv[1])

def _build():
    configs = get_configs(get_configs_path())

    build(configs["source"], configs["output"], configs["templates"], configs["mdb"])

def _live():
    configs = get_configs(get_configs_path())

    live(configs["source"], configs["output"], configs["templates"], configs["mdb"], configs["port"], configs["trigger_threshold"])
