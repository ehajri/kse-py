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


    def should_read():
        utcnow = datetime.datetime.utcnow
        if utcnow().weekday() == 4 or utcnow().weekday() == 5:
            return False
        elif utcnow().hour == 5 and utcnow().minute >= 40:
            return True
        elif utcnow().hour == 9 and utcnow().minute <= 45:
            return True
        elif utcnow().hour > 5 and utcnow().hour < 9:
            return True
        return False

    def obook():
        try:
            if should_read():
                read_obook()
            else:
                logger.info("obook: early?")
        except BaseException as e:
            logger.error("obook raised an exception:" + str(e))
        threading.Timer(10, obook).start()


    def timesale():
        try:
            if should_read():
                read_timesale()
            else:
                logger.info("timesale: early?")
        except BaseException as e:
            logger.error("timesale raised an exception:" + str(e))
        threading.Timer(10, timesale).start()

    def rquotes():
        try:
            if should_read():
                read_rquotes()
            else:
                logger.info("rquotes: early?")
        except BaseException as e:
            logger.error("rquotes raised an exception:" + str(e))
        threading.Timer(10, rquotes).start()

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
