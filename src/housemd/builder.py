from .generator import Generator
from os import path, listdir, mkdir
from shutil import rmtree, copy
import queue
import json

def update_metadatabase(mdb, file_path, md):
    key_arr = file_path.split(path.sep)
    _ = mdb

    for k in key_arr[:-1]:
        if k not in _:
            _[k] = dict()

        _ = _[k]

    _[key_arr[-1]] = md

def build(source_dir, out_dir, template_dir, metadatabase_path):
    """
    Build the static website

    metadatabase_path is the absolute path of the metadatabase file, it must contain the file name in the end. If metadatabase_path is None metadatabase is not dumped.
    """
    source_dir = path.abspath(source_dir)
    out_dir = path.abspath(out_dir)
    template_dir = path.abspath(template_dir)

    # Clean the out_dir generate all sub directories, also create the queue of markdown files and static files (using BFS)

    rmtree(out_dir)

    subdir_paths = queue.Queue()
    md_paths = queue.Queue()
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
    
    g = Generator(template_dir)
    mdb = dict()

    while not md_paths.empty():
        _ = md_paths.get()
        res, metadata = g(path.join(source_dir, _))
        y = path.splitext(_)
        y = "".join(y[:-1]) + ".html"

        with open(path.join(out_dir, y), "w") as f:
            f.write(res)

        update_metadatabase(mdb, y, metadata)

    # Copy all static files
    
    while not static_file_paths.empty():
        _ = static_file_paths.get()
        copy(path.join(source_dir, _), path.join(out_dir, _))

    # Dump the metadatabase

    if metadatabase_path is not None:
        with open(path.join(out_dir, metadatabase_path), "w") as f:
            f.write(json.dumps(mdb))
