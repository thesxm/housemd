import sys
from .builder import build
from os import path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from time import sleep, time
import threading
from http.server import SimpleHTTPRequestHandler
import socketserver

def _build():
    source_path, output_path, templates_path = map(path.abspath, sys.argv[1:4])
    mdb = None
    if len(sys.argv) > 4:
        mdb = sys.argv[4]

    print(f"building", end = "...")
    build(source_path, output_path, templates_path, mdb)
    print(f" done.")

class Handler(FileSystemEventHandler):
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

def _live():
    source_path, output_path, templates_path = map(path.abspath, sys.argv[1:4])
    
    _build()

    class StaticServerHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=output_path, **kwargs)

    http_server = socketserver.TCPServer(("", 8000), StaticServerHandler)
    server_thread = threading.Thread(target = _run_http_server, args = [http_server])
    server_thread.start()

    print("Static file server running")
    print(f"\tfrom: {output_path}")
    print(f"\tat: http://localhost:{8000}")

    observer = Observer()
    handler = Handler()

    observer.schedule(handler, source_path, recursive = True)
    observer.schedule(handler, templates_path, recursive = True)

    observer.start()
    print(f"listening for changes in {source_path} and {templates_path}")

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
