#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from data_init import BASE
from bs4 import BeautifulSoup

import json
import os
import shutil
import requests
from concurrent.futures import ThreadPoolExecutor

proxy_form = "{}://web-proxy.sgp.hpecorp.net:8080"
PROXY = {"http": proxy_form.format("http"), "https": proxy_form.format("https")}
# PROXY = {}
headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,zh-TW;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
        }
IMAGE_FOLDER = 'image/'


class ParseError(Exception):
    pass


def get_html(url):
    html = requests.get(url, headers=headers, proxies=PROXY).content
    return str(html, encoding='EUC-JP')


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
    print(url)
    r = requests.get(url, stream=True, proxies=PROXY)
    if r.status_code == 404:
        return False
    with open(os.path.join(IMAGE_FOLDER, fname), 'wb') as img:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, img)
    return True


def save_all_pm_image_no_alter(start, end):
    url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/{:0>3d}.png"
    for idx in range(start, end):
        save_single_image(url.format(idx), "{:0>3d}.png".format(idx))


def save_all_pm_image_alter(start, end):
    url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/{:0>3d}_f{}.png"

    for idx in range(start, end):
        alter = 1
        while save_single_image(url.format(idx, alter), "{:0>3d}_{}.png".format(idx, alter)) or alter == 1:
            alter += 1


def multi_scrapy(start, end, worker=20):
    jobs = []
    gap = (end - start)//worker
    with ThreadPoolExecutor(max_workers=worker) as pool:
        for cur_start in range(start, gap*worker, gap):
            cur_end = cur_start + gap
            if end - cur_end < gap:
                cur_end = end
            # jobs.append(pool.submit(save_all_pm_image_alter, cur_start, cur_end))
            jobs.append(pool.submit(save_all_pm_image_no_alter, cur_start, cur_end))
        for j in jobs:
            j.result()


if __name__ == "__main__":
    multi_scrapy(1, 893, 20)
    # save_all_pm_image_alter(892, 893)
    # whole = set(range(1, 831))
    # actual = set()
    #
    # for f in os.listdir(IMAGE_FOLDER):
    #     actual.add(int(f[:3]))
    #
    # for i in whole.difference(actual):
    #     save_all_pm_image_no_alter(i, i+1)

