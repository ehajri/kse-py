import sys, os
import threading
from common import *
from reader.read_rquotes import read_rquotes
from reader.read_timesale import read_timesale
from reader.read_obook import read_obook


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    def obook():
        read_obook()
        try:
            threading.Timer(10, obook).start()
        except Exception as e:
            logger.error("obook raised an exception:" + str(e))


    def timesale():
        read_timesale()
        try:
            threading.Timer(10, timesale).start()
        except Exception as e:
            logger.error("timesale raised an exception:" + str(e))

    def rquotes():
        read_rquotes()
        try:
            threading.Timer(10, rquotes).start()
        except Exception as e:
            logger.error("rquotes raised an exception:" + str(e))

    threading.Timer(0.1, obook).start()
    threading.Timer(0.1, timesale).start()
    threading.Timer(0.1, rquotes).start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)