from .builder import build
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from time import sleep
import threading

class FSEHandler(FileSystemEventHandler):
    def __init__(self, source_path, output_path, templates_path, mdb_path, trigger_threshold, *args, **kwargs):
        self.build_configs = [source_path, output_path, templates_path, mdb_path]
        self.trigger_threshold = trigger_threshold
        self._build_scheduler = [0, None]

        super().__init__(*args, **kwargs)

    def _event_validator(self, event):
        return event.is_directory and event.src_path in [self.build_configs[0], self.build_configs[2]]

    def _run_builder(self):
        self._build_scheduler[0] = 1
        print("build started.")
        build(*self.build_configs)
        print("build finished.")
        self._build_scheduler[1] = None
        self._build_scheduler[0] = 0

    def _trigger_build(self):
        if self._build_scheduler[0] == 0 and self._build_scheduler[1] is None:
            print("change detected.")

        if self._build_scheduler[0]:
            self._build_scheduler[1].join()

        if self._build_scheduler[1] is not None:
            self._build_scheduler[1].cancel()

        self._build_scheduler[1] = threading.Timer(self.trigger_threshold, self._run_builder)
        self._build_scheduler[1].start()

    def on_any_event(self, event):
        if not self._event_validator(event):
            return

        self._trigger_build()

def create_observer(source_path, output_path, templates_path, mdb_path, trigger_threshold):
    observer = Observer()
    handler = FSEHandler(source_path, output_path, templates_path, mdb_path, trigger_threshold)

    observer.schedule(handler, source_path, recursive = True)
    observer.schedule(handler, templates_path, recursive = True)

    return observer

def create_http_request_handler(output_path):
    class _(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory = output_path, **kwargs)

    return _

def create_http_server(output_path, port):
    class _(TCPServer):
        allow_reuse_address = True

    server = _(("", port), create_http_request_handler(output_path))

    return server

def live(source_path, output_path, templates_path, mdb_path, port, trigger_threshold):
    observer = create_observer(source_path, output_path, templates_path, mdb_path, trigger_threshold)
    server = create_http_server(output_path, port)

    server_thread = threading.Thread(target = server.serve_forever, daemon = True)
    
    print("initial build started.")
    build(source_path, output_path, templates_path, mdb_path)
    print("done.")
    print()
    print("Observing file changes in:")
    print(f"\tSource Directory: {source_path}")
    print(f"\tTemplates Directory: {templates_path}")
    print(f"\tTrigger Threshold: {trigger_threshold}")
    print()
    print("Starting HTTP server with configs:")
    print(f"\tDirectory: {output_path}")
    print(f"\tAddress: http://localhost:{server.server_address[1]}")
    print()

    observer.start()
    server_thread.start()

    try:
        while all([observer.is_alive(), server_thread.is_alive()]):
            sleep(.1)
    except:
        observer.stop()
        server.shutdown()
        server.server_close()
    finally:
        observer.join()
        server_thread.join()

