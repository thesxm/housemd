import sys
from .builder import build

def main():
    source_dir, out_dir, templates_dir = sys.argv[1:4]
    build(source_dir, out_dir, templates_dir)

if __name__ == "__main__":
    main()
