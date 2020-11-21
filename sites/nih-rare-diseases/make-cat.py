#!/usr/bin/python3
# make stat-pearl-cat.py
# derived from https://www.ncbi.nlm.nih.gov/books/NBK430685/

import os
import requests
from bs4 import BeautifulSoup
import json
import string
import iiab.adm_lib as adm

alpha_pages = []
disease_catalog = {}

with open('explore-html/diseases.html', 'r') as f:
    cat_html = f.read()

page = BeautifulSoup(cat_html, "html.parser")

#items = page.find_all(['li'])
#article_parts = page.find_all("div", {"class":"card"})
alpha_block = page.find('ul',{'class':'alpha-block-list'})
items = alpha_block.find_all(['li'])

for item in items:
    link = item.find('a')
    alpha_pages.append(link['href'])

# OR string.ascii_uppercase (but is string, not array) and 0-9

for sub_menu in alpha_pages:
    response = requests.get('https://rarediseases.info.nih.gov' +  sub_menu)
    response.encoding = 'utf-8'  # to be safe
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    list_block = soup.find('ul',{'class':'listing-diseases'})
    items = list_block.find_all(['li'])
    for item in items:
        print(item)
        try:
            link = item.find('a')
            url = link['href']
            disease_catalog[url] = link.text
        except:
            continue

# div id = what's new for new or changed articles


adm.write_json_file(disease_catalog, 'disease-catalog.json')
