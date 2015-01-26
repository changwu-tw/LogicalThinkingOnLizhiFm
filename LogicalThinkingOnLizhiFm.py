#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import ujson

from random import randint
from selenium import webdriver
from time import sleep

reload(sys)
sys.setdefaultencoding("utf-8")

PAGE_SITE = 'http://www.lizhi.fm/#/17248'
PAGE_PATTERN = 'http://www.lizhi.fm/#/17248/p/%s'


def downloadData():
    i = 1
    info = []

    while True:
        print "第 %s 頁: %s" % (i, PAGE_PATTERN % i)

        browser = webdriver.PhantomJS()
        browser.get(PAGE_PATTERN % i)
        page = browser.page_source

        pattern = r'data-url="(.*?)" data-cover'
        audioLinks = re.findall(pattern, page)

        if not audioLinks:
            break

        pattern = re.compile('<p title="(.*?)" class', re.U)
        audioNames = re.findall(pattern, page)

        for (name, link) in zip(audioNames, audioLinks):
            info.append({
                'name': name.replace('&quot;', ''),
                'link': link,
            })

        i += 1
        sleep(randint(1, 3))
    browser.quit()

    with open('podcast.json', 'w') as f:
        f.write(ujson.dumps(info, ensure_ascii=False))


def getLatestData():
    browser = webdriver.PhantomJS()
    browser.get(PAGE_SITE)
    page = browser.page_source
    browser.quit()

    pattern = r'data-url="(.*?)" data-cover'
    audioLinks = re.findall(pattern, page)

    pattern = re.compile('<p title="(.*?)" class', re.U)
    audioNames = re.findall(pattern, page)

    return audioLinks[0], audioNames[0]


def getHistoryData():
    with open('podcast.json', 'rb') as f:
        data = ujson.loads(f.read())
    return data[0]['link'], data


if __name__ == '__main__':
    if os.path.exists('podcast.json'):
        oldLink, info = getHistoryData()
        latestLink, latestName = getLatestData()

        if oldLink != latestLink:
            data = {
                'name': latestName,
                'link': latestLink,
            }
            info.insert(0, data)

            with open('podcast.json', 'w') as f:
                f.write(ujson.dumps(info, ensure_ascii=False))
    else:
        downloadData()
