#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup

def weather():
    url = "http://www.cwb.gov.tw/V7/forecast/taiwan/Taipei_City.htm"

    webfile = urllib.urlopen(url)
    webcontext = webfile.read()
    soup = BeautifulSoup(webcontext, "html.parser")
    table = soup.find("table", attrs={"class": "FcstBoxTable01"})
    result = []
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        temp = []
        for ele in cols:
            if ele.text.strip() == "":
                temp.append("http://www.cwb.gov.tw/V7/"+ele.img["src"][6:])
            else:
                temp.append(ele.text.strip())

        temp2 = {
                "fallback": "weather",
                "title": u"%s" % temp[2],
                "pretext": u"溫度：%s" % temp[0],
                "text": u"降雨機率%s" % temp[3],
                "thumb_url": temp[1]
            }
        result.append(temp2)
        break
    return result
