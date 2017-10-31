import requests
from bs4 import BeautifulSoup

link = 'http://english.mubasher.info/markets/KSE/stocks/NBK'






r = requests.get(link)

if r.status_code == requests.codes.ok:
    soup = BeautifulSoup(r.text)
    parentdiv = soup.find()
