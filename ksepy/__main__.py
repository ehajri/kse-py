import os
import sys
import threading
import traceback
from datetime import time
from common import *
from reader.read_obook import read_obook
from reader.read_rquotes import read_rquotes
from reader.read_timesale import read_timesale

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    def should_read():
        utcnow = datetime.datetime.utcnow()
        day = utcnow.weekday
        now = utcnow.time()
        if day not in [4, 5] and time(5, 40) <= now <= time(9, 45):
            return True
        return False

    def newcall(func):
        try:
            if should_read():
                func()
            else:
                logger.info(func.__name__ + " early?")
        except Exception as err:
            print(func.__name__ + " raised an error")
            traceback.print_tb(err.__traceback__)
            logger.error(func.__name__ + " raised an error")
            logger.error(traceback.extract_tb(err.__traceback__))
            errorlogger.error(func.__name__ + " raised an error")
            errorlogger.error(traceback.extract_tb(err.__traceback__))
        threading.Timer(10, newcall, args=(func)).start()
        
    threading.Timer(0.1, newcall, args=(read_obook)).start()
    threading.Timer(0.1, newcall, args=(read_timesale)).start()
    threading.Timer(0.1, newcall, args=(read_rquotes)).start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
