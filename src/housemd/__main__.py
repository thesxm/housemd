import sys
from .builder import build
from os import path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from time import sleep, time
import threading
from http.server import SimpleHTTPRequestHandler
import socketserver
import json

def _parse_config(config_file_path):
    config_data = json.load(open(config_file_path, "r"))

    try:
        for _ in ["source", "output", "templates"]:
            config_data[_] = path.abspath(config_data[_])
    except KeyError as e:
        raise BaseException(f"Invalid config file {config_file_path}, missing key {e.args[0]}")

    if "mdb" in config_data:
        config_data["mdb"] = path.abspath(config_data["mdb"])
    else:
        config_data["mdb"] = None

    return config_data

def _build():
    configs = _parse_config(sys.argv[1])

    print("building...")
    build(configs["source"], configs["output"], configs["templates"], configs["mdb"])
    print("\tdone.")

class EventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.build_sched = [None, 0]  # the build thread and build running status

    def __schedule_build(self, _):
        _[1] = 1
        _build()
        _[0] = None
        _[1] = 0

    def on_any_event(self, e):
        VALID_EVENTS = ["created", "modified", "deleted", "moved"]
        if e.event_type not in VALID_EVENTS or e.is_directory or e.src_path.endswith(".swp"):
            return

        if self.build_sched[0] is None:
            print()
            print(e.event_type, e.src_path, e.dest_path if e.event_type == "moved" else "")
        else:
            print(e.event_type, e.src_path, e.dest_path if e.event_type == "moved" else "")
            if self.build_sched[1]:
                self.build_sched[0].join()
            else:
                self.build_sched[0].cancel()
                self.build_sched[0] = None

        self.build_sched[0] = threading.Timer(3, self.__schedule_build, args = [self.build_sched])
        self.build_sched[0].start()

def _run_http_server(_):
    _.serve_forever()
    _.server_close()

def _create_server_handler_class(output_path):
    class _(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=output_path, **kwargs)

    return _

def _live():
    configs = _parse_config(sys.argv[1])
    
    _build()

    http_server = socketserver.TCPServer(("", 8000), _create_server_handler_class(configs["output"]))
    server_thread = threading.Thread(target = _run_http_server, args = [http_server])
    server_thread.start()

    print("Static file server running")
    print(f"\tserving: {configs['output']}")
    print(f"\tat: http://localhost:{8000}")

    observer = Observer()
    handler = EventHandler()

    observer.schedule(handler, configs["source"], recursive = True)
    observer.schedule(handler, configs["templates"], recursive = True)

    observer.start()
    print(f"listening for changes in source [{configs['source']} and templates [{configs['templates']}] directories")

    try:
        while observer.is_alive():
            sleep(1)
    except BaseException as e:
        print(f"ERROR: {e}")
        observer.stop()
        http_server.shutdown()
    finally:
        observer.join()
        server_thread.join()
        print("Stopped listening.")
