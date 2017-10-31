import sys

from configobj import ConfigObj

import scheduler
from app.ksepy.kse.News import NewsModel, FetchNews
from app.ksepy.kse.Obook import ObookModel, FetchObook
from app.ksepy.kse.Rquotes import RquotesModel, FetchRquotes
from app.ksepy.kse.Timesale import TimesaleModel, FetchTimesale
from app.ksepy.kse.kse import WebReader, Repo, logger
from app.ksepy.stock_models import Running

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
    logger.info("run obook started")
    web_reader = WebReader()

    url = config['obook']['url']
    dom_id = config['obook']['domId']

    fobook = FetchObook(url, dom_id, web_reader)
    obook = ObookModel(Running, fobook, Repo())
    obook.execute()
    logger.info("run obook finished")


def run_rquotes():
    logger.info("run rquotes started")
    web_reader = WebReader()

    url = config['rquotes']['url']
    dom_id = config['rquotes']['domId']

    frquotes = FetchRquotes(url, dom_id, web_reader)
    rquotes = RquotesModel(Running, frquotes, Repo())
    rquotes.execute()
    logger.info("run rquotes finished")


def run_timesale():
    logger.info("run timesale started")
    web_reader = WebReader()

    url = config['timesale']['url']
    dom_id = config['timesale']['domId']

    ftimesale = FetchTimesale(url, dom_id, web_reader)
    timesale = TimesaleModel(Running, ftimesale, Repo())
    timesale.execute()
    logger.info("run timesale finished")


def run_news():
    web_reader = WebReader()

    url = config['news']['url']
    dom_id = config['news']['domId']

    fnews = FetchNews(url, dom_id, web_reader)
    news = NewsModel(Running, fnews, Repo())
    news.execute()

if __name__ == "__main__":
    main()
