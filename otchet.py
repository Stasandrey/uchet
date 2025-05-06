#! /usr/bin/python3

import paho.mqtt.publish as publish
import requests
import json
from datetime import datetime
from datetime import timedelta
from datetime import date
from datetime import time

token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIwNTc3N2JjZjkyZWM0YTI2YjVmYWU0Z"
         "WFmNzYxZGZkYSIsImlhdCI6MTczNTM3ODM5MiwiZXhwIjoyMDUwNzM4MzkyfQ.q7yLekCN5_8_ju_w"
         "6A4oC22Tn2bfk8BvP79ksS9lC4o")
address = "http://192.168.100.77:8123/api/"
headers = {
    "Authorization": "Bearer %s" % token,
    "content-type": "application/json",
}
# hours = "history/period/2024-11-15T10:00:00+03:00?end_time=2024-11-15T10:10:00&filter_entity_id=sensor.pokazaniia_aktivnoi"
hour = "history/period/"
sensor = "&filter_entity_id=sensor.pokazaniia_aktivnoi"
data = []

def ask(req):
    response = requests.get(address + req, headers=headers)
    #print(response)
    return response.text

def one_hour(now):
    td = now.strftime("%Y-%m-%dT%H:%M:%S+03:00")
    ld = (now + timedelta(hours=1)).strftime("?end_time=%Y-%m-%dT%H:%M:%S")
    hours = hour + td + ld + sensor
    #    print(hours)
    answer = json.loads(ask(hours))[0]
    #    print(answer)
    #    print(answer[0]['state'])
    #    print(answer[len(answer) - 1]['state'])
    #    print(float(answer[len(answer) - 1]['state']) - float(answer[0]['state']))

    # print(td)
    # print(ld)
    # result1 = float(answer[1]['state'])
    # result2 = float(answer[len(answer) - 1]['state']) - float(answer[0]['state'])
    # print(result1, '   ', result2)
    t = (now + timedelta(hours = 1) ).strftime("%H:%M")
    pok = round(float(answer[len(answer) - 1]['state']), 3)
    delta = round(float(answer[len(answer) - 1]['state']) - float(answer[0]['state']), 3)
    s = { 'time':t, 'pok':pok, 'delta':delta }
    data.append(s)

def main():

    now = datetime.now()
    period = datetime.combine( now.date() - timedelta(days = 1 ), time(00, 00, 00) )
    period = period - timedelta(hours = 1)
    print(period)
    item = 0
    while item in range(0, 25):
        # print(period)
        one_hour( period )
        period = period + timedelta( hours=1)
        item = item + 1
#    publish.single('hour', str(result), hostname="127.0.0.1")
    for item in data:
        print(item)

if __name__ == "__main__":
    main()
