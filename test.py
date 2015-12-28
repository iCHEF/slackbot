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

from hello import hello_msg

from response import Response
# encoding=utf-8
import jieba
import jieba.posseg as pseg
# general = C024FEN2R
# test room C0E6X8ELB

BIND_CH = ["C0HE01E2Y"]

# 關鍵字列表，當句子中相關的詞彙時，使用該詞彙相關的功能
KEYWORD_LIST = {
    '午餐,晚餐':search.search_eat,
    '新片,電影':movie.get_movie,
    '天氣':weather.weather,
    '機器':hello_msg,
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
    用結巴切字詞並分出詞性，回傳每一個字詞都是包含內容跟詞性的list
    https://gist.github.com/luw2007/6016931  詞性分析
    '''
    word_list = []
    words = pseg.cut(msg_text)
    for word, flag in words:
        word_list.append(dict(value=word, flag=flag))
    return word_list

def msg_handler(msgs):
    '''
    handle message to decide which function should be executed and which message would this function execute
    '''
    execute_function = None
    executed_msg = None
    for msg in msgs:
        executed_msg = msg
        if "channel" not in msg:  # If no channel info in this msg, ignore this msg
            continue
        if "ts" not in msg:  # If no timestamp in this msg, ignore this msg
            continue
        if "text" not in msg:  # If no message text in this msg, ignore this msg
            continue
        if abs(float(msg["ts"]) - time.time()) < 90:  # If this message is 90 second before, ignore this message
            word_list = cut_msg(msg["text"])  # 得到切好的詞
            print word_list
            for word_with_flag in word_list:
                if word_with_flag['flag'] == 'n':  # Use noun in message text to decide which function should be executed
                    for keyword in KEYWORD_LIST.keys():
                        if word_with_flag['value'].encode('utf-8') in keyword:  # If the noun in message match the KEYWORD set above, run the function belong that keyword
                            execute_function = KEYWORD_LIST[keyword]
                            return [execute_function ,executed_msg]

            return [execute_function ,executed_msg]

    return [execute_function, executed_msg]


if __name__=='__main__':
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini')) # load your slack token in config.ini
    token = config.get("ichef", "token")  # found at https://api.slack.com/web#authentication
    slack_client = SlackClient(token)
    if slack_client.rtm_connect():
        while True:
            messages = slack_client.rtm_read()
            execute_function, msg = msg_handler(messages)
            if execute_function is not None:
                response = execute_function(msg['text'])
                if isinstance(response, Response):  # check if function return regular response type
                    response_args = response.get_args(msg['channel'])
                else:
                    raise InputError("wrong response type")
                slack_client.api_call("chat.postMessage", **response_args)

            time.sleep(1)
    else:
        print "Connection Failed, invalid token?"
