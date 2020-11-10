#!/usr/bin/python3
# make stat-pearl-cat.py
# derived from https://www.ncbi.nlm.nih.gov/books/NBK430685/

import os
import requests
from bs4 import BeautifulSoup
import json
import iiab.adm_lib as adm

stat_pearl_catalog = {}

with open('stat-pearl-catalog.html', 'r') as f:
    cat_html = f.read()

page = BeautifulSoup(cat_html, "html.parser")

items = page.find_all(['li'])

for i, item in enumerate(items):
    # has class of form 'toc_itm_NBK430685_' but NBK430685 is not the nih code which in this case is 554556
    # actually NBK430685 is the number of the catalog, not the article and is in every <li>
    links = item.find_all(['a', 'link'])
    for j, link in enumerate(links):
        if link.has_attr('href'):
            url = link['href']
            if 'article-' in url:
                article_id = url.split('article-')[1].split('/')[0]
                article_info = {'url': url, 'title': link.text}
                stat_pearl_catalog[article_id] = article_info

adm.write_json_file(stat_pearl_catalog, 'stat-pearl-catalog.json')
