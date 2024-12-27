import sys
from .builder import build

def main():
    source_dir, out_dir, templates_dir = sys.argv[1:4]

    if len(sys.argv) == 5:
        mdp = sys.argv[4]
    else:
        mdp = None

    build(source_dir, out_dir, templates_dir, metadatabase_path = mdp)

if __name__ == "__main__":
    main()
