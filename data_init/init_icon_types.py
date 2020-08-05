#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from data_init import BASE
from bs4 import BeautifulSoup

import json
import os
import shutil
import requests

proxy_form = "{}://web-proxy.sgp.hpecorp.net:8080"
PROXY = {"http": proxy_form.format("http"), "https": proxy_form.format("https")}
# PROXY = {}
headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,zh-TW;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
        }
IMAGE_FOLDER = 'images/'


class ParseError(Exception):
    pass


class HtmlParser(object):
    def __init__(self, html_path=None, html_str=None):
        if html_path is not None:
            with open(html_path, "rt", encoding="utf8") as f:
                html_str = f.readlines()
        self.bs = BeautifulSoup(''.join(html_str), features="html.parser")

    def yield_img_url(self):
        for a in self.bs.find_all('a', attrs={'class': ["image"]}):
            png_name = a['href'].split(':')[-1]
            url = 'https:' + a.find('img')['src'].replace('64px', '96px')
            yield url, png_name


def save_single_image(url, fname):
    r = requests.get(url, stream=True, proxies=PROXY)
    with open(os.path.join(IMAGE_FOLDER, fname), 'wb') as img:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, img)


if __name__ == '__main__':
    for u, f in HtmlParser(os.path.join(BASE, "data/icons.html")).yield_img_url():
        save_single_image(u, f)
