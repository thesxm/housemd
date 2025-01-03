from os import mkdir, path
import json

def _take_input(q, default):
    inp = input(q)
    if inp == "":
        return default

    return inp

def init():
    configs = dict()

    _ = _take_input("Config file name (housemd-config.json): ", "housemd-config.json")
    print("\n{")
    configs["source"] = path.abspath(_take_input("\tSource directory path (content): ", "content"))
    configs["output"] = path.abspath(_take_input("\tOutput direcotry path (public): ", "public"))
    configs["templates"] = path.abspath(_take_input("\tTemplates directory path (templates): ", "templates"))
    configs["mdb"] = path.abspath(_take_input(f"\tMetadatabase path ({configs['output']}/mdb.json): ", path.join(configs["output"], "mdb.json")))
    configs["port"] = int(_take_input("\thousemd-live HTTP server port (None, automatically assigned): ", 0))
    configs["trigger_threshold"] = float(_take_input("\thousemd-live trigger threshold (2 seconds): ", 2.0))
    print("}\n")

    for k in ["source", "output", "templates"]:
        print(f"Creating {k} directory [{configs[k]}].")
        try:
            mkdir(configs[k])
        except OSError:
            print("\tFailed, maybe the directory already exists?")
        else:
            print("\tDone.")

    with open(_, "w") as o:
        json.dump(configs, o)

    print("\nhousemd initialized succesfully.")
