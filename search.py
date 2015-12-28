#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google import google


def search_eat(query_msg):
    num_page = 2
    search_results = google.search(query_msg, num_page, lang='zh-Hant')
    return_result = []
    for result in search_results:
        temp = {
            "fallback": "movie",
            "title": result.name,
            "title_link": result.link,
        }

        return_result.append(temp)

    return return_result
