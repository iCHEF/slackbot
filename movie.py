#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup

def week_movie():
    url = "https://tw.movies.yahoo.com/movie_thisweek.html"

    webfile = urllib.urlopen(url)
    webcontext = webfile.read()
    soup = BeautifulSoup(webcontext, "html.parser")
    lis = soup.findAll("div", attrs={"class": "clearfix row"})
    result = []
    for li in lis:
        movie_date = li.find("span", {"class": "date"}).text
        test = li.find("a")
        temp = {
                "fallback": "movie",
                "title": test.img["title"],
                "title_link": test["href"],
                "text": movie_date,
                "thumb_url": test.img["src"]
            }
        result.append(temp)
    return result


def top_movie():
    url = "https://tw.movies.yahoo.com/chart.html?cate=taipei"

    webfile = urllib.urlopen(url)
    webcontext = webfile.read()
    soup = BeautifulSoup(webcontext, "html.parser")
    lis = soup.findAll("td", attrs={"class": "c3"})
    result = []
    for li in lis:
        title = li.find("a").text
        if li.find("a").text == "":
            title = li.find("img")["title"]
        link = li.find("a")["href"]

        temp = {
                "fallback": "movie",
                "title": title,
                "title_link": link,
            }
        result.append(temp)
    return result
