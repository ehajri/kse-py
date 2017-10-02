import requests, peewee
from bs4 import BeautifulSoup
from kse import stock_models as sm
from configobj import ConfigObj
import logging, sys, datetime

#logging.basicConfig(stream=sys.stderr, level=logging.INFO)
#logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def console_logger(name, level=logging.INFO):
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

logger = console_logger('CONSOLE')
errorlogger = setup_logger('EXCEPTION', '/tmp/kse.log')

config = ConfigObj('config.ini')

class WebReader:
    @staticmethod
    def read(link):
        f = requests.get(link)
        soup = BeautifulSoup(f.text, 'html.parser')
        return soup


def do_bulk_insert_pw(model, records, fields):
    """
    :param model:
    :param records:
    :param fields (list):
    :return:
    """
    logger.debug("Writing %s in to the database.", len(records))
    data_source = [dict(zip(fields, t)) for t in records]
    with sm.db.atomic():
        for idx in range(0, len(data_source), 100):
            try:
                model.insert_many(data_source[idx:idx + 100]).execute()
            except peewee.IntegrityError:
                pass


def sanitize(str):
    return str.strip().replace(',', '')

def change_types(records):
    try:
        for i in [0, 6, 7]:
            records[i] = 0 if not records[i] else int(records[i])
        for i in [1, 2, 3, 4, 5, 8, 9, 10, 12, 13]:
            records[i] = 0 if not records[i] else float(records[i])

        records[11] = datetime.datetime.strptime(records[11], "%d-%m-%Y").date()
        return records
    except Exception as e:
        logging.warning(records, str(e))
    return None