from bs4 import BeautifulSoup
import requests

parameters = {}
parameters['ctl00$ContentMatter$txtFrom'] = '01/01/2016'
parameters['ctl00$ContentMatter$txtTo'] = '12/31/2016'
parameters['__EVENTVALIDATION'] ='jnf90ASalXKM0YOiN30pHjha9s1678tYLjpF5nMF6xaOC8Diy4ooHps6/sw7ZQPHRYhsDURJCCZgosLymI7/8S/ZOQuPspDb7gYhufY7yHaqd7wLbRjFOZXXo3DJVWfYgMtoYGWrZy4AxiQQ7LSY3x9u1tdpxXgeQ91l5/vN2E0Mm+Y/B9uTSe4Qd0iYLHGPMkCthp4jok9pAtunwUKYkPP88BSGLO1w9iKHTlKXU9T5pLS7'
parameters['__VIEWSTATE'] ='6J7WFNn7MXGyuMVaFzaBkqo3oNuL4yV/YXVNZq7CFe2KFTZI9unW3XYIn0IGx62gprODJNlRjfVt2kzTV4ZOoXtLd/ANKXjG1QFKL3/uNO9bGpDMLm0zQKWaS7Xd4AMdnuVr7UBDjEWupvHHIaJk3ma4lCNEllu8MleedHHOL1DoBdVhoXJYtpcljMmTwUqYs+AplPU4SStYT5gRCVTXQJYwZYeXKd+8/0DN/mMy6WutS7aeCaKmxo70gBRQtVbxVEJPFV5ogktNSWhYlNwnn8qDxlTCZORhXV2W4nQY/DHyMOo8erFKDJd7BawF7OfzvuumAoP4CkMskLbuMgimFZpQdwa78ACTUk1MJ2//WKMbgbaJvB9DkenhAgTrue8i48W29ZGXWdQE7226HxAhqhgYGhU7aZbHVyKYppr6sGDxggTGPE4LgrZ+z6zlIPzAQR/iFF+Jr3MliMLmlNLD2p0O3wASnMaeC5iqjz0vUGUaGs1JrmF9ceKsqKdJeNbj12Dl7rmKL6SB6WgKguc8CPKjnMHSHsp/rqkrj4Ck1lb1HFN1Ee9cukeX92J7Xxq/X786LQlqHyUU00zxmOStCNyRgr2+jMBZtBfahczIZr6gOFHms7Afqy1hWoGbdNLHCV1BwkUUuJ1ycL/5gl5qFFuwh/8vfdy4FAtmFs/YKoRGXSloc8P5/Po7b9N4JuTbKkgPPn9pFCQe+XFnohdbiccxtdGfzih5ZFQdIVeM/bnS/4dAZWFAgHhDO7JvFxCPYwz0FD5G1k0EKyEb5h0zhYDw0+YGhz/NAhZIYOaXAjNkipfPE82FJdSlePhNh6B2re5uSeNNxzORWfFLThfMsWK1OHEcEQC6HepPnZ2rMGBA1uukxsBJ2bzhG7kcD6pwoFSHL/Y9B2RBIvE0m5JmMZy/qrJFz2SJ+bZp8A6Uk1CzmtsQs65ucjz84mwQFZMKJAX4FlvwYqep9aFsiUDIiHUTqr1rq/vH5r/6jaYfWkOYwR0D1S0h6mvJ3rpBM+Pxhx4WNJD/PcRaXIT+D6t5nFA0+XGHCKzWYWbNPZuNhDvvjj5c8WeqGF4bQA4TdMFkMXHU2qp/1zn8DIF7M9rClaWSnz/xmZh65e/xaZg+YuQ0p6oGuNYlpmPfvDIfiO7JIlexMpbRMjFI43+8x0podJz+/Z5PyhOHIfpeAwQGgTIPQYf8DSj8LLOGU/2ue+hCkyNXvBDlO6WeryAHQPT1LqacoP5v2ellQ2fmIA5OnpNc9+yIL+MyncoNWSb55+/mamqV48sv3+W5VBENS9sGKrC1JxdLfL7g/JfEzekGA4E9b8PmwLZynX7coLRpRhvqrsggDCQ3USSjYHOYonv9PUVouIvI7y49v6RmcTQxzrMWW0geaIJ6kDFeMon6ZQuM0Xstyrd2Nk2oopN665vPNPBLEvmFwnhq+m8kqHWuJYJIirXEgnubvTVtyzmgQsyu6TW8/XzMqZ4CriTUX7gRSq5b0dznSotIAZU3HSJmq7gSOmYv5eo1B/+abbeDTqO4dSu6q0mIKBelZzgcDkYkyay9DpIum7yK4nk5GNEEwrmQsJKu6QNgWgejjGhM5nHdTrGTe4PHdlh+RIzpXKJsvrK7sVC+HF0/PaohuHLSxTsEZg+J+qGiIaVW7g/dw3I498OJi8jlGRKsrspHW0y/MnsDIOQ='

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