#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time     : 2020/5/17
# @Author   : Peng
# @Desc

import scrapy, json, pymysql, re
from urllib import parse
from scrapy.http import FormRequest
from invest.localSettings import db_mysql
from invest.items import InvestShareHolderItem, InvestBusinessIcItem


class CptIcProSpider(scrapy.Spider):

    name = 'chuangtouicprofile'
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

    db = None
    cursor = None

    pre_url = "https://primary-market.aigauss.com"

    url_data = {
        "uuid": "",
    }

    common_headers = {
        ":method": "GET",
        ":path": "/primary-market-pro-v3/ic_info/query?{}".format(parse.urlencode(url_data)),

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
        "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI5YWUxOThlZS1iMjk1LTQyOTctOWU2Ni0wY2ZmODU5MGJiMzciLCJqdGkiOiIiLCJ3anRpIjoiIiwiZGV2aWNlIjoiMyIsInByb2R1Y3QiOiI1IiwiaXNzIjoidGlnZXJvYm8uY29tIiwiYXVkIjoidGlnZXJvYm8iLCJleHAiOjE2MjA2NDEzMTB9.BWHMmq1IZgP-X7dT7zTa76TYPkeOVIWsXx9Tpz25crs",
        "userid": "9ae198ee-b295-4297-9e66-0cff8590bb37",
        "user-agent": "26/android/8.0.0/MIX 2S/Wx+nj9YIiYEDAHajZZ0GuYay/mi",
        "accept-encoding": "gzip",
    }


    def __init__(self):
        self.db = pymysql.connect(host=db_mysql['host'], user=db_mysql['user'], password=db_mysql['passwd'],
                                  db=db_mysql['db'],
                                  port=3306, charset=db_mysql['charset'])
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)


    def start_requests(self):

        sql = '''
            select id, company_uuid from `invest_project_profile` where id > 0 and id <= 10000 limit 10000;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db.commit()
        self.cursor.close()
        self.db.close()

        if data is not None and len(data) > 0:
            for comp_uuid in data:
                uuid = comp_uuid['company_uuid']
                if '' != uuid:
                    self.url_data['uuid'] = uuid
                    self.common_headers[':path'] = "/primary-market-pro-v3/ic_info/query?{}".format(parse.urlencode(self.url_data))

                    yield FormRequest(self.pre_url + "/primary-market-pro-v3/ic_info/query", method="GET", headers=self.common_headers,
                                      formdata=self.url_data, callback=self.parse, dont_filter=False)

        return []




    def parse(self, response):
        if 200 == response.status:
            out_data = json.loads(response.body.decode('utf-8'))
            if 200 == out_data['status'] and out_data['result'] is not None:
                result_data = out_data['result']
                shareholder = result_data['companyShareholderVos']
                if shareholder is not None and len(shareholder) > 0:
                    for holder_item in shareholder:
                        sto_holder_item = InvestShareHolderItem()

                        if '-' == holder_item['capital_contribution']:
                            sto_holder_item['capital_contribution'] = 0.0000
                        else:
                            sto_holder_item['capital_contribution'] = holder_item['capital_contribution']

                        sto_holder_item['name'] = holder_item['name']
                        sto_holder_item['shareholder_type'] = holder_item['shareholder_type']

                        if '-' == holder_item['date_contribution']:
                            sto_holder_item['date_contribution'] = "1970-01-01"
                        else:
                            sto_holder_item['date_contribution'] = holder_item['date_contribution']

                        sto_holder_item['ratio'] = holder_item['ratio']

                        yield sto_holder_item

                company_info = result_data['company']
                if company_info is not None and len(company_info) > 0:

                    company_item = InvestBusinessIcItem()
                    company_item['company_type'] = company_info['company_type']
                    company_item['registration_authority'] = company_info['registration_authority']
                    if '-' == company_info['approval_date']:
                        company_item['approval_date'] = "1970-01-01"
                    else:
                        company_item['approval_date'] = company_info['approval_date']

                    company_item['legal_person'] = company_info['legal_person']
                    company_item['registered_address'] = company_info['registered_address']
                    company_item['business_term'] = company_info['business_term']
                    company_item['uscc'] = company_info['uscc']

                    if '-' == company_info['insurer_num']:
                        company_item['insurer_num'] = int(0)
                    else:
                        company_item['insurer_num'] = int(company_info['insurer_num'])

                    print(">>>>>>>>>", company_item['insurer_num'])

                    company_item['industry'] = company_info['industry']

                    company_item['company_name_used'] = company_info['company_name_used']
                    company_item['registration_num'] = company_info['registration_num']

                    if '-' == company_info['registered_capital']:
                        company_item['registered_capital'] = 0.0000
                    else:
                        company_item['registered_capital'] = str(re.search(r'\d+\.?\d*', str(company_info['registered_capital'])).group())


                    if str(company_info['registered_capital']).find(r'人民币') == -1:
                        company_item['currency_type'] = 2
                    else:
                        company_item['currency_type'] = 1

                    company_item['operating_scope'] = company_info['operating_scope']
                    company_item['uuid'] = company_info['uuid']
                    company_item['operating_state'] = company_info['operating_state']

                    if '-' == company_info['contributed_capital']:
                        company_item['contributed_capital'] = 0.0000
                    else:
                        company_item['contributed_capital'] = str(re.search(r'\d+\.?\d*', str(company_info['contributed_capital'])).group())

                    company_item['company_name'] = company_info['company_name']
                    if '-' == company_info['setup_date']:
                        company_item['setup_date'] = '1970-01-01'
                    else:
                        company_item['setup_date'] = company_info['setup_date']

                    company_item['company_url'] = company_info['company_url']
                    company_item['company_name_en'] = company_info['company_name_en']
                    company_item['org_code'] = company_info['org_code']

                    yield company_item

        else:
            self.logger.warning("peng. these is no content")





