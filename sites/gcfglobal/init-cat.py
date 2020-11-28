#!/usr/bin/python3

import os,sys
import requests
from bs4 import BeautifulSoup
import json
import string
import uuid
from copy import deepcopy
import iiab.adm_lib as adm
#import pdb; pdb.set_trace()

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
      "zip_etag": "",
      "zip_size": "",
      "zip_last_modified": "",
      "file_count": "0"
    }

WORKING_DIR = "/library/working/rachel"
GCFGLOBAL = 'https://edu.gcfglobal.org/en/download/all'

if not os.path.isdir(WORKING_DIR + '/download-all.html'):
   r = requests.get(GCFGLOBAL)
   if r.status_code == 200:
      with open(WORKING_DIR + '/download-all.html','w') as fp:
         fp.write(r.text)
   else:
      print("failed to open source: %s"%GCFGLOBAL)
      sys.exit(1)

with open(WORKING_DIR + '/download-all.html', 'r') as f:
    cat_html = f.read()

page = BeautifulSoup(cat_html, "html.parser")

content = page.find('div',{'id':'content'})
topic_list = content.find_all('li',{"class":"supercollection"})
print(len(topic_list))
for super_topic in topic_list:
    category = super_topic.a.text
    items_list = super_topic.find('ul')
    items = items_list.find_all('a')
    for item in items:
        title = item.text
        print(title)
        zip_url = item['href']
        moddir = zip_url.split('/')[-1]
        moddir = moddir.split('.zip')[0]
        if moddir[0:3] == 'tr_':
            moddir = moddir[3:]
        else:
            moddir = 'en-' + moddir
        r = requests.get(zip_url)
        if r.status_code == 200:
            head = r.headers
            zip_etag = head['etag']
            zip_size = head['content-length']
            zip_last_modified = head['last-modified']
        else:
            zip_etag = ""
            zip_size = ""
            zip_last_modified = ""

        item_info = {}
        item_info = deepcopy(item_base)

        item_info['module_id'] = str(uuid.uuid4())
        item_info['moddir'] = moddir
        item_info['category'] = category
        item_info['title'] = title
        item_info['lang'] = moddir[0:2] # may not work for Chinese
        item_info['zip_http_url'] = zip_url
        item_info['zip_size'] = zip_size
        item_info['zip_last_modified'] = zip_last_modified
        item_info['zip_etag'] = zip_etag

        gcf_catalog[moddir + '-' + category] = item_info


adm.write_json_file(gcf_catalog, 'gcf-catalog.json')
with open(WORKING_DIR + "/gcf-catalog.json",'w') as fp:
    fp.write(json.dumps(gcf_catalog, indent=2, sort_keys=True))
