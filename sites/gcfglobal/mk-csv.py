#!/usr/bin/python3

import os,sys
import requests
from bs4 import BeautifulSoup
import json
import string
import uuid
from copy import deepcopy
import iiab.adm_lib as adm

gcf_catalog = {}
item_base = {
      "rating": "",
      "age_range": "adult",
      "zip_ftp_url": "",
      "module_id": "xxx",
      "is_hidden": "No",
      "moddir": "en-xxx",
      "category": "xxx",
      "title": "",
      "prereq_id": "",
      "version": "1.0",
      "ksize": "0",
      "logo_url": "",
      "type": "html",
      "description": "",
      "index_mod_sample_url": "",
      "source_url": "",
      "rsync_url": "",
      "lang": "en",
      "prereq_note": "",
      "zip_http_url": "",
      "file_count": "0"
    }

with open('download-all.html', 'r') as f:
    cat_html = f.read()

page = BeautifulSoup(cat_html, "html.parser")


super_collection = page.findAll('li',{'class':'supercollection all-topics'})
print("lenght of super_collection: %s"%len(super_collection))
for collection in super_collection:
   name = collection.find('a')
   print()
   #print(name.string)
   items = collection.findAll('a')
   for item in items:
      if item.get('href','') != '':
         print("%s,%s,%s"%(name.string,item.string, item['href']))
   #header = collection.find_all('a')
   #print(header[0].string)
   

#topics = topic_list.find_all('ul',{'class':'level-1'})
 
sys.exit(1)

for topic in topics:
    category = topic.li.a.text
    print(category)
    items = topic.ul.find_all('li')
    for item in items:
        title = item.a.text
        print(title)
        zip_url = item.a['href']
        moddir = zip_url.split('/')[-1]
        moddir = moddir.split('.zip')[0]
        if moddir[0:3] == 'tr_':
            moddir = moddir[3:]
        else:
            moddir = 'en-' + moddir

        item_info = {}
        item_info = deepcopy(item_base)

        item_info['module_id'] = str(uuid.uuid4())
        item_info['moddir'] = moddir
        item_info['category'] = category
        item_info['title'] = title
        item_info['category'] = category
        item_info['lang'] = moddir[0:2] # may not work for Chinese
        item_info['category'] = category
        item_info['zip_http_url'] = zip_url

        gcf_catalog[moddir] = item_info


adm.write_json_file(gcf_catalog, 'gcf-catalog.json')
