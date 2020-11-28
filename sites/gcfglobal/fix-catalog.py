#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create a sqlite database from oer2go-cat.json


import os
import sys
import sqlite3
import json
import hashlib
from subprocess import Popen, PIPE
#import pdb; pdb.set_trace()


# Globals
db = object
WORKING_DIR = '/library/working/rachel'
gcf_catalog = {}

def get_module_json(path):
    with open(path,'r') as fp:
        modules = json.loads(   fp.read())
    return modules

def put_module_json(path):
    with open(path,'w') as fp:
        modules = fp.write(json.dimps(gcf_catalog,indent=2))

def main():
    for item in gcf_catalog:
        #gcf_catalog[item]['requires_update'] = "True"
        #gcf_catalog[item]['zip_md5'] = ""
        gcf_catalog[item]['source_url'] = gcf_catalog[item]['zip_http_url']
        gcf_catalog[item]['zip_http_url'] = ""

###########################################################
if __name__ == "__main__":
   cat = WORKING_DIR + '/gcf-catalog.json'
   gcf_catalog = get_module_json(cat)
   

   main()
   #print(json.dumps(gcf_catalog,indent=2, sort_keys=True))
   with open(cat,'w') as fp:
        fp.write(json.dumps(gcf_catalog,indent=2,sort_keys=True))
