#!/usr/bin/python3
import os
import re

from basicspider.spider import BasicSpider
from basicspider.spider import LOGGER, logging, set_log_level
import iiab.adm_lib as adm
set_log_level(logging.DEBUG)

# PARAMS
################################################################################
site = 'www.ncbi.nlm.nih.gov'
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
stat_pearl_catalog = {}
stat_pearl_catalog = adm.read_json('stat-pearl-catalog.json')

test_cnt = 5
for article_id in stat_pearl_catalog:
    original_url = MAIN_SOURCE_DOMAIN + stat_pearl_catalog[article_id]['url']
    local_file = original_url.split('://')[1]
    if local_file[-1] == '/':
        local_file = local_file[:-1] + '.html'
    else:
        local_file = local_file + '.html'

    local_dir = os.path.dirname(local_file)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    if os.path.isfile(local_file):
        continue
    # print(original_url)
    url, html = crawler.download_page(original_url)
    if html is None:
        print('Skipping ' + article_id)
        continue
    with open(local_file, 'w') as f:
        f.write(html)

    crawler.do_one_page(url, html, spider=False)
    test_cnt -= 1
    if test_cnt == 0:
        break

crawler.post_crawl_output()
