#!/usr/local/bin/python3
from configobj import ConfigObj
import pymysql.cursors, json

config = ConfigObj('config.ini')

def GetRecords():
    result = []
    connection = pymysql.connect(host=config['db']['host'],
                             user=config['db']['user'],
                             passwd=config['db']['pass'],
                             db=config['db']['dbname2'],
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM jsons WHERE uri LIKE '%listed-companies%kw%'")
            result = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
        return result

def getsome(jsonStr):
    jsonObj = json.loads(jsonStr)
    return (jsonObj['url'], jsonObj['profileUrl'], jsonObj['symbol'])

def pythonize(records):
    return ((getsome(record['json']), record['lang'], record['uri']) for record in records)

for i in pythonize(GetRecords()):
    print(i)
