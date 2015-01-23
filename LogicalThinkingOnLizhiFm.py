#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import sys

from random import randint
from selenium import webdriver
from time import sleep

reload(sys)
sys.setdefaultencoding("utf-8")

PAGE_PATTERN = 'http://www.lizhi.fm/#/17248/p/%s'


if __name__ == '__main__':

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
        f.write(json.dumps(info, ensure_ascii=False))

