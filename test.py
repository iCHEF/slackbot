#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from datetime import datetime
from slackclient import SlackClient
import search
import json
import movie
import random
import weather
import ConfigParser
import jieba
# general = C024FEN2R
# test room C0E6X8ELB

BIND_CH = ["C0E6X8ELB"]
jieba.add_word(u"六都", freq=None, tag=None)

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
        "username": u"愛雪芙卍美食卍羅伯特".encode("utf-8"),
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
        "username": u"愛雪芙卍電影卍羅伯特".encode("utf-8"),
        "as_user": False,
        "attachments": json.dumps(attachments)
    }
    sc.api_call("chat.postMessage", **args)


def send_weather_msg(sc, channel, msg):
    city = list(jieba.cut(msg))
    city.remove(u"天氣")
    attachments = weather.weather2(city[0])
    if city[0] == u"六都":
        text = u"愛雪芙氣象報告".encode("utf-8")
    else:
        text = city[0].encode("utf-8")
    args = {
        "channel": channel,
        "text": text,
        "username": u"愛雪芙卍天氣卍羅伯特".encode("utf-8"),
        "as_user": False,
        "attachments": json.dumps(attachments)
    }
    sc.api_call("chat.postMessage", **args)


def send_hello_msg(sc, channel, msg):

    if u"我愛你" in msg:
        text = u"人家... 人家才不愛你呢！哼！！"
    else:
        text = u"你... 你一直叫我，我也不會理你的喲 >////<"

    args = {
        "channel": channel,
        "text": text.encode("utf-8"),
        "username": u"愛雪芙羅伯特".encode("utf-8"),
        "as_user": False,
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
            if u"天氣" in jieba.cut(msg["text"]) and msg["channel"] in BIND_CH:
                return {"status": True, "channel": msg["channel"], "args": msg["text"], "types": "weather"}
            if u"羅伯特" in msg["text"] and msg["channel"] in BIND_CH:
                return {"status": True, "channel": msg["channel"], "args": msg["text"], "types": "Robot"}
    return {"status": False, "channel": None}

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
token = config.get("ichef", "token")  # found at https://api.slack.com/web#authentication
sc = SlackClient(token)
if sc.rtm_connect():
    while True:
        if datetime.now().hour == 22 and datetime.now().minute == 51 and datetime.now().second == 0:
            send_weather_msg(sc, "C024FEN2R", u"六都天氣")
        result = msg_handler(sc.rtm_read())
        if result["status"] is True:
            if result["types"] == "eat":
                send_eat_msg(sc, result["channel"], result["args"])
            if result["types"] == "movie":
                send_movie_msg(sc, result["channel"])
            if result["types"] == "top_movie":
                send_movie_msg(sc, result["channel"], is_top=True)
            if result["types"] == "weather":
                send_weather_msg(sc, result["channel"], result["args"])
            if result["types"] == "Robot":
                send_hello_msg(sc, result["channel"], result["args"])
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
