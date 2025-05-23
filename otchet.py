#! /usr/bin/python3

import requests
import json
from datetime import datetime
from datetime import timedelta
from datetime import time

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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

    answer = json.loads(ask(hours))[0]

    t = (now + timedelta(hours = 1) ).strftime("%H:%M")
    pok = round(float(answer[len(answer) - 1]['state']), 3)
    delta = round(float(answer[len(answer) - 1]['state']) - float(answer[0]['state']), 3)
    s = { 'time':t, 'pok':pok, 'delta':delta }
    data.append(s)
def calculate():
    now = datetime.now()
    period = datetime.combine(now.date() - timedelta(days=1), time(00, 00, 00))
    per = period.date().strftime('%d.%m.%Y')
    period = period - timedelta(hours=1)
    print(period)
    item = 0
    while item in range(0, 25):
        # print(period)
        one_hour(period)
        period = period + timedelta(hours=1)
        item = item + 1
    #
    for item in data:
        print(item)
    return per

def build_pdf(per):
    xlist = [70, 150, 280, 410, 550]
    ylist = [750]
    for i in range(0,26):
        ylist.append(75 + i * 25)
    ylist.append(75)
    w, h = A4
    c = canvas.Canvas("/home/andrey/homeassistant/data.pdf", pagesize=A4)
    c.drawString(250, 760, per)

    text1 = c.beginText(85, 708)
    text2 = c.beginText(190, 708)
    text3 = c.beginText(320, 708)
    text4 = c.beginText(450,708)
    text1.setLeading(25)
    text2.setLeading(25)
    text3.setLeading(25)
    text4.setLeading(25)
    text1.textLine('Time')
    text2.textLine('Pokazaniya')
    text3.textLine('Delta')
    text4.textLine('Real')
    s_delta = 0
    s_real = 0
    for i in range(0,len(data)):
        text1.textLine(data[i]['time'])
        text2.textLine(str(data[i]['pok']))
        if i!=len(data) - 1:
            text3.textLine( str( data[i+1]['delta'] ) )
            text4.textLine( str ( round( data[i+1]['delta'] * 60, 2) ) )
            s_delta = s_delta + data[i+1]['delta']
            s_real = s_real + data[i + 1]['delta'] * 60

        else:
            text3.textLine('')
            text4.textLine('')

    text3.textLine( str(s_delta) )
    text4.textLine( str( round(s_real, 2) ) )

    c.drawText(text1)
    c.drawText(text2)
    c.drawText(text3)
    c.drawText(text4)
    c.grid(xlist, ylist)
    c.showPage()
    c.save()

def main():
    per = calculate()
    build_pdf(per)

if __name__ == "__main__":
    main()
