import sys
from reader.read_rquotes import read_rquotes
from reader.read_timesale import read_timesale
from reader.read_obook import read_obook
def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    read_obook()

if __name__ == "__main__":
    main()
