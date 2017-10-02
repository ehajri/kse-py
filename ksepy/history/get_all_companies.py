from bs4 import BeautifulSoup
from models.ksehistory import Company, database
import requests
import timeit

start_time = timeit.default_timer()


def getelapsed():
    return timeit.default_timer() - start_time


def get_company_list():
    req = requests.post("http://www.boursakuwait.com.kw/Stock/Companies.aspx")
    timer_page = getelapsed()

    print(req.status_code, req.reason)

    data = req.text

    soup = BeautifulSoup(data, 'html.parser')

    table = soup.find(id='ContentMatter_GridView1')

    if table is None:
        print('table does not exit')
        exit()

    trs = table.findAll('tr')
    trs.pop(0)
    companies = [[td.text for td in tr.findAll('td')] for tr in trs]

    print('There are', len(companies), 'companies')

    fields = "stk ticker name sector".split(' ')
    data_source = [dict(zip(fields, t)) for t in companies]

    timer_process = getelapsed() - timer_page

    print(data_source)
    with database.atomic():
        Company.insert_many(data_source).execute()

    timer_db = getelapsed() - timer_page - timer_process

    print('loading page took', timer_page, 'seconds')
    print('processing took', timer_process, 'seconds')
    print('writing to db took', timer_db, 'seconds')

get_company_list()

