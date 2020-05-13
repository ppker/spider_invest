#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time     : 2020/5/11
# @Author   : Peng
# @Desc

import scrapy, json, pymysql
from urllib import parse

from scrapy.http import FormRequest
from invest.localSettings import db_mysql

class CptProSpider(scrapy.Spider):

    name = 'chuangtouprofile'
    allowed_domains = ['primary-market.aigauss.com']

    custom_settings = {
        "DOWNLOAD_DELAY": 1.8,
        "LOG_ENABLED": True,
        "COOKIES_ENABLES": False,
        "CONCURRENT_REQUESTS": 8,

        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 'invest.middlewares.RotateUserAgentMiddleware': 400,
        },
        "FEED_EXPORT_ENCODING": 'utf-8',  # feed export 导出json文件 中文不乱码
    }

    url_data = {
        "uuid": ""
    }
    # https://primary-market.aigauss.com/primary-market-pro-v3/ic_info/query?uuid=0462e393ee0d4018936db2d5f08a3263
    # https://primary-market.aigauss.com/primary-market-pro-v3/project_info/query/v4?uuid=ae5ef44099b9465bbaae5e932437636f

    common_headers = {
        ":method": "GET",
        ":path": "/primary-market-pro-v3/project_info/query/v4?{}".format(parse.urlencode(url_data)),

        ":authority": "primary-market.aigauss.com",
        ":scheme": "https",
        "app-version": "26",
        "version-name": "1.3.0",
        "manufacturer": "Xiaomi",
        "model": "MIX 2S",
        "os": "android",
        "os-version": "8.0.0",
        "device-id": "Wx+nj9YIiYEDAHajZZ0GuYay",
        "device": "3",
        "product": "5",
        "screen-width": "392",
        "screen-height": "738",
        "channel": "mi",
        "content-type": "application/json",
        "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIxYzY0YmM4MC1iNDkzLTQ4NmEtYWI2ZC0yOTFjN2NlYTNiODgiLCJqdGkiOiIiLCJ3anRpIjoiIiwiZGV2aWNlIjoiMyIsInByb2R1Y3QiOiI1IiwiaXNzIjoidGlnZXJvYm8uY29tIiwiYXVkIjoidGlnZXJvYm8iLCJleHAiOjE2MjA4MDAyOTl9.jjD2YsOUnSTXARLf66x9aJbWuR6GhSm1Vu84h_uusIE",
        "userid": "1c64bc80-b493-486a-ab6d-291c7cea3b88",
        "user-agent": "26/android/8.0.0/MIX 2S/Wx+nj9YIiYEDAHajZZ0GuYay/mi",
        "accept-encoding": "gzip",
    }

    db = None
    cursor = None

    pre_url = "https://primary-market.aigauss.com"


    def __init__(self):
        self.db = pymysql.connect(host=db_mysql['host'], user=db_mysql['user'], password=db_mysql['passwd'], db=db_mysql['db'],
                                  port=3306, charset=db_mysql['charset'])
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)



    def start_requests(self):

        # 先获取1000条uuid
        sql = '''
            select id, uuid from `invest_project_all_list` where id > 0 and id <= 1000 limit 1000; 
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db.commit()
        self.cursor.close()
        self.db.close()

        if data is not None:
            for uuid_data in data:
                uuid = uuid_data['uuid']
                if "" != uuid:
                    self.url_data['uuid'] = uuid
                    self.common_headers[':path'] = "/primary-market-pro-v3/project_info/query/v4?{}".format(parse.urlencode(self.url_data)),
                    yield FormRequest(self.pre_url + "/primary-market-pro-v3/project_info/query/v4", method="GET", headers=self.common_headers,
                                      formdata=self.url_data, callback=self.parse, dont_filter=False)

            return []



    def parse(self, response):
        if 200 == response.status:
            out_data = json.loads(response.body.decode('utf-8'))
            if 200 == out_data['status'] and len(out_data['result']) > 0:
                result_data = out_data['result']
                projectNewsList = result_data['projectNewsList']['data']
                if len(projectNewsList) > 0:
                    for news in projectNewsList:









