# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem



class InvestPipeline:

    def __init__(self, db_mysql):
        dbparms = {"cursorclass": pymysql.cursors.DictCursor, "use_unicode": True}
        dbparms.update(db_mysql)

        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(db_mysql=crawler.settings.get('DB_MYSQL'))


    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        return item


    def handle_error(self, failure, item, spider):
        spider.logger.warning("peng. this has errors")
        insert_sql, params = item.get_insert_sql()

        spider.logger.warning("sql is >>>>>> \n")
        spider.logger.warning(str(insert_sql) % params)
        spider.logger.warning(failure)


    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        print("peng. 开始执行插入语句")
        cursor.execute(insert_sql, params)


    def close_spider(self, spider):
        self.dbpool.close()






