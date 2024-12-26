from .generator import Generator
from os import path, listdir, mkdir
from shutil import rmtree, copy
import queue

def build(source_dir, out_dir, template_dir):
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

    # Use Generator to generate html files of the md files in md_paths queue and store them in out_dir
    
    g = Generator(template_dir)
    while not md_paths.empty():
        _ = md_paths.get()
        res = g(path.join(source_dir, _))
        y = path.splitext(_)
        y = "".join(y[:-1]) + ".html"
        y = path.join(out_dir, y)

        with open(y, "w") as f:
            f.write(res)

    # Copy all static files
    
    while not static_file_paths.empty():
        _ = static_file_paths.get()
        copy(path.join(source_dir, _), path.join(out_dir, _))
