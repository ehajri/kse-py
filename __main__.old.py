import sys
from kse.Obook import ObookModel, FetchObook
from kse.Timesale import TimesaleModel, FetchTimesale
from kse.News import NewsModel, FetchNews
from kse.Rquotes import RquotesModel, FetchRquotes
from kse.kse import WebReader, Repo
from kse.stock_models import Running, Rquotes, News, Obook, Timesale
from configobj import ConfigObj
import scheduler

config = ConfigObj('../config.ini')


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    scheduler.periodic(scheduler.scheduler, 10, run_obook())
    scheduler.periodic(scheduler.scheduler, 10, run_news())
    scheduler.periodic(scheduler.scheduler, 10, run_rquotes())
    scheduler.periodic(scheduler.scheduler, 10, run_timesale())
    scheduler.scheduler.run()


def run_obook():
    web_reader = WebReader()

    url = config['obook']['url']
    dom_id = config['obook']['domId']

    fobook = FetchObook(url, dom_id, web_reader)
    obook = ObookModel(Running, fobook, Repo())
    obook.execute()


def run_rquotes():
    web_reader = WebReader()

    url = config['rquotes']['url']
    dom_id = config['rquotes']['domId']

    frquotes = FetchRquotes(url, dom_id, web_reader)
    rquotes = RquotesModel(Running, frquotes, Repo())
    rquotes.execute()


def run_timesale():
    web_reader = WebReader()

    url = config['timesale']['url']
    dom_id = config['timesale']['domId']

    ftimesale = FetchTimesale(url, dom_id, web_reader)
    timesale = TimesaleModel(Running, ftimesale, Repo())
    timesale.execute()


def run_news():
    web_reader = WebReader()

    url = config['news']['url']
    dom_id = config['news']['domId']

    fnews = FetchNews(url, dom_id, web_reader)
    news = NewsModel(Running, fnews, Repo())
    news.execute()

if __name__ == "__main__":
    main()
