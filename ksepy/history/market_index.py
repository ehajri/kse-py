from bs4 import BeautifulSoup
import requests

parameters = {}
parameters['ctl00$ContentMatter$txtFrom'] = '04/01/2016'
parameters['ctl00$ContentMatter$txtTo'] = '12/31/2016'
parameters['__EVENTVALIDATION'] ='hlKTQ1Mtb52qheN3u8TfROWT0WYv0YFeVn6DirOu/juGSx/F/sG/mUXnkW6HRGfyHJHYdKQMYUbHsEtXVxwZ+t65GKiDWCXmJvBww84IitA5iMFjO8togVFmiYrUcwNl/zIVKWN2lMGseqpOB+fRyyL3PK5T5gvJvPB7EF1y/MeFWTLjg05JpjuAyavG/jHoTwspvXS1BiIMN/J9QMEXkbpf2H9+KhRecdZ1QntU1MsKdro4'
parameters['__VIEWSTATE'] ='PNngztipVIkBeO17Ujybs5dWywq4Qpuag7G3Quu2kUkcNo8MLGOzEh6TZORrcG+r2s71/FzSU88H0Y/m+6txqNU6DrW2i8lpK9ZCc4A727m84bNS5lgdKNXa5v0HeTLkTz2r9KShW/Ux33YhMneaqELgA8mHTeoDoNdAURqseKHu//5bOt9KudMS8gMsMxN9IYkonPOyDemSWFI7CYja4mc4PPUyvMdhh6fWeTie0CcxdL9pskVw3WO6q570uDPSqoxXpR0IYQh6zZLaNpJPmGC49nG1FbVl5ylqXhnuLA1CpOO0o85bhmA5CDuRfTIOtdLwRB+tNih/vqFmUvWCQd+JgJ68ZxyuWhXZSLHIOPIo/VUs/9Rolxi91AdAdch1IRo/IL+mGawqwbf1xLGXGltQF9E='
parameters['ctl00$ContentMatter$Button1'] = 'SHOW'

req = requests.post("http://www.boursakuwait.com.kw/History/MarketIndex.aspx", parameters)

print(req.status_code, req.reason)

data = req.text


soup = BeautifulSoup(data, "html.parser")

table = soup.find(id='ContentMatter_HistoryGRID')
if table is None:
    print('table does not exist')
    exit()

trs = table.findAll('tr')

trs.pop(0)

print("table has", len(trs), "records")
