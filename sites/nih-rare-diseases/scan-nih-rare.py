#!/usr/bin/python3
import os
import re

from basicspider.spider import BasicSpider
from basicspider.spider import LOGGER, logging, set_log_level
import iiab.adm_lib as adm
set_log_level(logging.DEBUG)

# PARAMS
################################################################################
site = 'rarediseases.info.nih.gov'
MAIN_SOURCE_DOMAIN = 'https://' + site
START_PAGE = 'https://' + site
SOURCE_DOMAINS = []
IGNORE_URLS = []
crawler = BasicSpider(main_source_domain=MAIN_SOURCE_DOMAIN)
crawler.IGNORE_URLS.extend(IGNORE_URLS)

crawler.set_output_file_names(site)
crawler.pre_crawl_setup()
crawler.read_global_site_json()

crawler.SHORTEN_CRAWL = True
disease_catalog = {}
disease_catalog = adm.read_json('disease-catalog.json')

test_cnt = 5
for disease_url in disease_catalog:
    original_url = MAIN_SOURCE_DOMAIN + disease_url
    local_name = disease_url[1:].replace('/', '.')
    local_file = 'raw/html/' + local_name + '.html'

    local_dir = os.path.dirname(local_file)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    if os.path.isfile(local_file):
        continue
    # print(original_url)
    url, html = crawler.download_page(original_url)
    if html is None:
        print('Skipping ' + disease_url)
        continue
    with open(local_file, 'w') as f:
        f.write(html)

    crawler.do_one_page(url, html, spider=False)

    # cheat to do all pages
    # test_cnt -= 1

    if test_cnt == 0:
        break

crawler.post_crawl_output()

# to modify

#for i in soup.find('div', {"id":None}).findChildren():
#    i.replace_with('##')

#with open("example_modified.html", "wb") as f_output:
#    f_output.write(soup.prettify("utf-8"))
