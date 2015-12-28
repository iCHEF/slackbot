#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from slackclient import SlackClient
import search
import json
import movie
import random
import weather
import ConfigParser
# general = C024FEN2R
# test room C0E6X8ELB

BIND_CH = ["C024FEN2R"]


def send_eat_msg(sc, channel, args):
    check = args.split(" ")
    is_random = False
    query_msg = u"晴光商圈 美食"
    if len(check) > 1:
        if u"幫選" in check:
            is_random = True
            check.remove(u"幫選")
        if len(check) > 1:
            query_msg = " ".join(check[1:])

    eat_result = search.search_eat(query_msg)
    if is_random is True:
        choose = random.randint(1, len(eat_result) - 1)
        attachments = [eat_result[choose]]
    else:
        attachments = eat_result

    args = {
        "channel": channel,
        "text": eat_result[choose]["title"].encode("utf-8"),
        "username": u"愛雪芙羅伯特".encode("utf-8"),
        "as_user": False,
        "attachments": json.dumps(attachments)
    }
    sc.api_call("chat.postMessage", **args)


def send_movie_msg(sc, channel, is_top=False):
    if is_top:
        attachments = movie.top_movie()
    else:
        attachments = movie.week_movie()
    args = {
        "channel": channel,
        "text": "Hey Guys",
        "username": u"愛雪芙羅伯特".encode("utf-8"),
        "as_user": False,
        "attachments": json.dumps(attachments)
    }
    sc.api_call("chat.postMessage", **args)


def send_weather_msg(sc, channel, is_top=False):
    if is_top:
        attachments = weather.weather()
    else:
        attachments = weather.weather()
    args = {
        "channel": channel,
        "text": "Hey Guys",
        "username": u"愛雪芙羅伯特".encode("utf-8"),
        "as_user": False,
        "attachments": json.dumps(attachments)
    }
    sc.api_call("chat.postMessage", **args)


def msg_handler(msgs):
    for msg in msgs:
        if "channel" not in msg:
            continue
        if "ts" not in msg:
            continue
        if "text" not in msg:
            continue
        if abs(float(msg["ts"]) - time.time()) < 90:
            if msg["text"][:2] == u"吃啥" and msg["channel"] in BIND_CH:
                return {"status": True, "channel": msg["channel"], "args": msg["text"], "types": "eat"}
            if msg["text"] == u"本週新片" and msg["channel"] in BIND_CH:
                return {"status": True, "channel": msg["channel"], "args": None, "types": "movie"}
            if msg["text"] == u"本週排行" and msg["channel"] in BIND_CH:
                return {"status": True, "channel": msg["channel"], "args": None, "types": "top_movie"}
            if msg["text"] == u"天氣" and msg["channel"] in BIND_CH:
                return {"status": True, "channel": msg["channel"], "args": None, "types": "weather"}
    return {"status": False, "channel": None}

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
token = config.get("ichef", "token")  # found at https://api.slack.com/web#authentication
sc = SlackClient(token)
if sc.rtm_connect():
    while True:
        result = msg_handler(sc.rtm_read())
        if result["status"] is True:
            if result["types"] == "eat":
                send_eat_msg(sc, result["channel"], result["args"])
            if result["types"] == "movie":
                send_movie_msg(sc, result["channel"])
            if result["types"] == "top_movie":
                send_movie_msg(sc, result["channel"], is_top=True)
            if result["types"] == "weather":
                send_weather_msg(sc, result["channel"], is_top=True)
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
