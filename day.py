#! /usr/bin/python3

import paho.mqtt.publish as publish
import requests
import json
from datetime import datetime
from datetime import timedelta

token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI0OWJkYzIwZDk3YjA0OGRjYTY3ZmI4N"
         "mJiOTAwY2Q4OSIsImlhdCI6MTczMTczNjI3MiwiZXhwIjoyMDQ3MDk2MjcyfQ.CYhf3K3yhWlDGobM"
         "_DrXgidw2ZKbfD0Qu2fof_TVtQk")
address = "http://192.168.100.77:8123/api/"
headers = {
    "Authorization": "Bearer %s" % token,
    "content-type": "application/json",
}
# hours = "history/period/2024-11-15T10:00:00+03:00?end_time=2024-11-15T10:10:00&filter_entity_id=sensor.pokazaniia_aktivnoi"
hour = "history/period/"
sensor = "&filter_entity_id=sensor.pokazaniia_aktivnoi"


def ask(req):
    response = requests.get(address + req, headers=headers)
    return response.text


def main():
    now = datetime.now()
    td = now.strftime("?end_time=%Y-%m-%dT%H:%M:%S")
    ld = (now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S+03:00")
    hours = hour + ld + td + sensor
#    print(hours)
    answer = json.loads(ask(hours))[0]
#    print(answer)
#    print(answer[0]['state'])
#    print(answer[len(answer) - 1]['state'])
#    print(float(answer[len(answer) - 1]['state']) - float(answer[0]['state']))

#    print(td)
#    print(ld)
    result = float(answer[len(answer) - 1]['state']) - float(answer[0]['state'])
    publish.single('day', str(result), hostname="127.0.0.1")

if __name__ == "__main__":
    main()
