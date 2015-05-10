import requests
from bs4 import BeautifulSoup

def FetchURL(link):
    "Reads the URL and fetch its content"
    f = requests.get(link)

    if f.status_code == 200:
        soup = BeautifulSoup(f.text)
        return soup
    else:
        return None

def Fetch(link, id):
    soup = FetchURL(link)
    if soup is None:
        return None

    dom = soup.find(id=id)
    if dom is None:
        return None

    if dom.name == 'table':
        array = []
        for tr in dom.findAll('tr'):
            trarray = []
            for td in tr.findAll('td'):
                trarray.append(td)

    return dom
