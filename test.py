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
# encoding=utf-8
import jieba
# general = C024FEN2R
# test room C0E6X8ELB

BIND_CH = ["C0E6X8ELB"]

# 關鍵字列表，當句子中相關的詞彙時，使用該詞彙相關的功能
KEYWORD_LIST = {
    '午餐,晚餐':search.search_eat,
    '新片,排行':movie.top_movie,
    '天氣':weather.weather,
}

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


def send_weather_msg(sc, channel, city):

    attachments = weather.weather(city)
    args = {
        "channel": channel,
        "text": city[3:].encode("utf-8"),
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


def cut_msg(msg_text):
    '''
    用結巴切字詞，並回傳切好的字詞的list
    '''
    seg_list = jieba.cut(msg_text, cut_all=False)
    text_list = "$$".join(seg_list)  # 精确模式
    return text_list.split("$$")

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
            if msg["text"][:2] == u"天氣" and msg["channel"] in BIND_CH:
                return {"status": True, "channel": msg["channel"], "args": msg["text"], "types": "weather"}
            if u"羅伯特" in msg["text"] and msg["channel"] in BIND_CH:
                return {"status": True, "channel": msg["channel"], "args": msg["text"], "types": "Robot"}
    return {"status": False, "channel": None}


if __name__=='__main__':
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini')) # load your slack token in config.ini
    token = config.get("ichef", "token")  # found at https://api.slack.com/web#authentication
    slack_client = SlackClient(token)
    if slack_client.rtm_connect():
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
                    send_weather_msg(sc, result["channel"], result["args"])
                if result["types"] == "Robot":
                    send_hello_msg(sc, result["channel"], result["args"])
            time.sleep(1)
    else:
        print "Connection Failed, invalid token?"
