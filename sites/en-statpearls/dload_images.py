#!/usr/bin/python3

import os,string, sys
import json
import requests
import iiab.adm_lib as adm


site = 'www.statpearls.com'
url_json_file = site + '_urls.json'
page_json_file = site + '_pages.json'
redirects_json_file = site + '_redirects.json'
ignored_urls_json_file = site + '_ignored_urls.json'
error_urls_json_file = site + '_error_urls.json'

site_urls = adm.read_json(url_json_file)

dnld_count = 5
for url in site_urls:
    content_type = site_urls[url].get('content-type', '')
    content_type = content_type.strip()
    if 'image' in content_type:
        if 'pictures/getimagecontent' in url:
            link = url
            if link[-1] == '/':
                link = link[:-1]
            filename = link.rsplit('/')[-1]
            if content_type == 'image/jpeg':
                filename += '.jpg'
            else:
                filename += '.' + content_type.split('/')[1]

            local_file = 'en-statpearls/pictures/' + filename

            local_dir = os.path.dirname(local_file)
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)

            if os.path.isfile(local_file):
                continue

            resp = requests.get(url)
            print(url)
            print(local_file)
            image = resp.content
            if resp.status_code == 200:
                with open(local_file, 'wb') as f:
                    f.write(image)

            #dnld_count -= 1
            if dnld_count == 0:
                break
