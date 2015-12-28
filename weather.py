#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup

CITY_DICTIONARY = {
    u"台北市":"Taipei_City",
    u"台北":"Taipei_City",
    u"新北市":"New_Taipei_City",
    u"新北":"New_Taipei_City",
    u"台中市":"Taichung_City",
    u"台中":"Taichung_City",
    u"台南市":"Tainan_City",
    u"台南":"Tainan_City",
    u"高雄市":"Kaohsiung_City",
    u"高雄":"Kaohsiung_City",
}

def weather(city):
    location = CITY_DICTIONARY.get(city[3:],None)
    if location is None:
        return [{
                "fallback": "weather",
                "title": u"機器人壞掉惹",
                "text": city[3:] + u"什麼的人家聽不懂啦QAQ"
            }]
    url = "http://www.cwb.gov.tw/V7/forecast/taiwan/"+location+".htm"
    
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
