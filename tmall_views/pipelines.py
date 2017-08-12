# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
import datetime

def insert_data(date, views):
    conn = sqlite3.connect('tmall_views.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS views
                 (date text PRIMARY KEY, views integer)''')

    # Insert a row of data
    try:
        c.execute("INSERT INTO views VALUES ('{0}',{1})".format(date, views))
    except sqlite3.IntegrityError:
        pass
    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

class TmallViewsPipeline(object):
    def process_item(self, item, spider):
        if item['item_name'] == '访问':
            insert_data(datetime.date.today(), item['item'])
        return item
