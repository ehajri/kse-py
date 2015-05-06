import time, datetime, sys, os

def Process():
    print(datetime.datetime.now())
    time.sleep(19)
    Process()

if __name__ == '__main__':
    try:
        Process()
    except KeyboardInterrupt:
        print('Interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
