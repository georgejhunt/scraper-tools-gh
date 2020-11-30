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
WORKING_DIR = "/library/www/html/modules/gcf"
gcf_catalog = {}

class Sqlite():
   def __init__(self, filename):
      self.conn = sqlite3.connect(filename)
      self.conn.row_factory = sqlite3.Row
      self.conn.text_factory = str
      self.c = self.conn.cursor()

   def __del__(self):
      self.conn.commit()
      self.c.close()
      del self.conn

def get_module_json(path):
    with open(path,'r') as fp:
        modules = json.loads(   fp.read())
    return modules


def create_sqlite_table():
   db.c.execute("CREATE TABLE if not exists modules (id INTEGER PRIMARY KEY,"\
      "perma_ref TEXT, rating TEXT, age_range TEXT, zip_ftp_url TEXT,"\
      "module_id TEXT, is_hidden TEXT, moddir TEXT, category TEXT, "\
      "title TEXT, prereq_id TEXT, version TEXT, ksize TEXT, logo_url TEXT,"\
      "type TEXT, description TEXT, index_mod_sample_url TEXT, source_url TEXT,"\
      "rsync_url TEXT, lang TEXT, prereq_note TEXT, zip_http_url TEXT,"\
      "zip_size TEXT, zip_last_modified TEXT, zip_etag TEXT, file_count TEXT)"\
      )
   db.c.execute('CREATE UNIQUE INDEX IF NOT EXISTS module_id_idx ON  modules (module_id)')

def update_record(cat_item,perma_ref):
      rating = cat_item['rating']
      age_range = cat_item['age_range']
      zip_ftp_url = cat_item['zip_ftp_url']
      module_id = cat_item['module_id']
      is_hidden  = cat_item['is_hidden']
      moddir = cat_item['moddir']
      category = cat_item['category']
      title = cat_item['title']
      prereq_id = cat_item['prereq_id']
      version = cat_item['version']
      ksize = cat_item['ksize']
      logo_url = cat_item['logo_url']
      type = cat_item['type']
      description = cat_item['description']
      index_mod_sample_url = cat_item['index_mod_sample_url']
      source_url = cat_item['source_url']
      rsync_url = cat_item['rsync_url']
      lang = cat_item['lang']
      prereq_note = cat_item['prereq_note']
      zip_http_url = cat_item['zip_http_url']
      zip_size = cat_item['zip_size']
      zip_last_modified = cat_item['zip_last_modified']
      zip_etag = cat_item['zip_etag']
      file_count = cat_item['file_count']
    
      sql = "insert or replace into modules ("\
          "perma_ref, rating, age_range, zip_ftp_url,"\
          "module_id, is_hidden, moddir, category, "\
          "title, prereq_id, version, ksize, logo_url,"\
          "type, description, index_mod_sample_url, source_url,"\
          "rsync_url, lang, prereq_note, zip_http_url,"\
          "zip_size, zip_last_modified, zip_etag, file_count)"\
          "values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
      db.c.execute(sql,(perma_ref, rating, age_range, zip_ftp_url,
          module_id, is_hidden, moddir, category, 
          title, prereq_id, version, ksize, logo_url,
          type, description, index_mod_sample_url, source_url,
          rsync_url, lang, prereq_note, zip_http_url,
          zip_size, zip_last_modified, zip_etag, file_count))

def main():
    for item in gcf_catalog:
        update_record(gcf_catalog[item],item)

###########################################################
if __name__ == "__main__":
   ########### database operations ##############
   db = Sqlite(WORKING_DIR + '/modules.sqlite')
   db.c.execute('drop table if exists modules')
   create_sqlite_table()
   gcf_catalog = get_module_json(WORKING_DIR + '/gcf-catalog.json')

   main()
