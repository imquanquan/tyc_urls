# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

URL_FILE = "urls.txt"

class TianyanchaPipeline(object):
    def process_item(self, item, spider):
        with open(URL_FILE, "a") as f:
            f.write(item['url'] + '\n')
        return item
