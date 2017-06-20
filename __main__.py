import sys
from kse.Obook import ObookModel, FetchObook
from kse.Timesale import TimesaleModel, FetchTimesale
from kse.News import NewsModel, FetchNews
from kse.Rquotes import RquotesModel, FetchRquotes
from configobj import ConfigObj
from kse.kse import WebReader

config = ConfigObj('../config.ini')

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]


def Obook():
    web_reader = WebReader()

    url = config['obook']['url']
    dom_id = config['obook']['domId']

    fobook = FetchObook(url, dom_id, web_reader)
    obook = ObookModel()

if __name__ == "__main__":
    main()
