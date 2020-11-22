#!/usr/bin/python3

import os
import requests
from bs4 import BeautifulSoup
import json
import string
import iiab.adm_lib as adm

alpha_pages = []
gcf_catalog = {}

with open('download-all.html', 'r') as f:
    cat_html = f.read()

page = BeautifulSoup(cat_html, "html.parser")


topic_list = page.find('ul',{'class':'all-topics'})

topics = topic_list.find_all('li',{'class':'all-topics'})
for topic in topics:
    category = topic.li.a.text
    print(category)
    items = topic.ul.find_all('li')
    for item in items:
        name = item.a.text
        zip_url = item.a['href']
        gcf_catalog[name] = {'category': category, 'zip-url': zip_url}


adm.write_json_file(gcf_catalog, 'gcf-catalog.json')
