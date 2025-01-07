from .generator import Generator
from os import path, listdir, mkdir
from shutil import rmtree, copy
import queue
import json
import threading

def update_metadatabase(mdb, file_path, md):
    key_arr = file_path.split(path.sep)
    _ = mdb

    for k in key_arr[:-1]:
        if k not in _:
            _[k] = dict()

        _ = _[k]

    _[key_arr[-1]] = md

def _run_thread(ind, source_dir, out_dir, template_dir, md_paths, mdb_queue):
        g = Generator(template_dir)
        while not md_paths.empty():
            _ = md_paths.get()
            res, metadata = g(path.join(source_dir, _))
            y = path.splitext(_)
            y = "".join(y[:-1]) + ".html"

            with open(path.join(out_dir, y), "w") as f:
                f.write(res)

            mdb_queue.put((y, metadata))

def build(source_dir, out_dir, template_dir, metadatabase_path, build_thread_count):
    """
    Build the static website

    metadatabase_path is the absolute path of the metadatabase file, it must contain the file name in the end. If metadatabase_path is None metadatabase is not dumped.
    """
    source_dir = path.abspath(source_dir)
    out_dir = path.abspath(out_dir)
    template_dir = path.abspath(template_dir)
    metadatabase_path = path.abspath(metadatabase_path) if metadatabase_path is not None else None

    # Clean the out_dir generate all sub directories, also create the queue of markdown files and static files (using BFS)

    try:
        rmtree(out_dir)
    except:
        pass

    subdir_paths = queue.Queue()
    md_paths = queue.Queue()
    mdb_queue = queue.Queue()
    static_file_paths = queue.Queue()

    subdir_paths.put("")
    while not subdir_paths.empty():
        _ = subdir_paths.get()
        mkdir(path.join(out_dir, _))

        for x in listdir(path.join(source_dir, _)):
            y = path.join(_, x)
            if path.isdir(path.join(source_dir, y)):
                subdir_paths.put(y)
            elif path.splitext(path.join(source_dir, y))[-1] == ".md":
                md_paths.put(y)
            else:
                static_file_paths.put(y)

    # Use Generator to generate html files of the md files in md_paths queue and store them in out_dir while updating the metadatabase
    
    build_threads = []
    for i in range(build_thread_count):
        try:
            t = threading.Thread(target = _run_thread, args = (i, source_dir, out_dir, template_dir, md_paths, mdb_queue))
            t.start()
        except:
            print("Error while spawning thread, skipping.")
        else:
            build_threads.append(t)

    if len(build_threads) > 0:
        print(f"spawned {len(build_threads)} threads.")
        for i in range(len(build_threads)):
            build_threads[i].join()
    else:  # If no threads were able to be spawned, build in the current thread
        print(f"failed to spawn any new thread, building in the current one.")
        _run_thread(-1, source_dir, out_dir, template_dir, md_paths, mdb_queue)

    mdb = dict()
    while not mdb_queue.empty():
        update_metadatabase(mdb, *mdb_queue.get())

    # Copy all static files
    
    while not static_file_paths.empty():
        _ = static_file_paths.get()
        copy(path.join(source_dir, _), path.join(out_dir, _))

    # Dump the metadatabase

    if metadatabase_path is not None:
        with open(metadatabase_path, "w") as f:
            f.write(json.dumps(mdb))
