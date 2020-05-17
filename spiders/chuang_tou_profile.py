#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time     : 2020/5/11
# @Author   : Peng
# @Desc

import scrapy, json, pymysql, re
from urllib import parse

from scrapy.http import FormRequest
from invest.localSettings import db_mysql
from invest.items import InvestNewsListItem, InvestProjectItem, InvestCoreMemberItem, InvestFinanceRecordItem

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
            select id, uuid from `invest_project_all_list` where id > 0 and id <= 10000 limit 10000; 
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

                # 新闻文章数据表
                if len(projectNewsList) > 0:
                    for news in projectNewsList:
                        item = InvestNewsListItem()

                        item['project_name'] = news['name']
                        item['publish_time'] = news['publish_time']
                        item['bundle_key'] = news['bundle_key']
                        item['source'] = news['source']
                        item['title'] = news['title']
                        item['type'] = news['type']
                        item['uuid'] = news['uuid']

                        yield item

                # 项目竞品数据

                competitors_container = ''
                competitors_str = ''
                competitors_data = result_data['projectCompetitors']['data']
                if len(competitors_data) > 0:
                    for competi in competitors_data:
                        competitors_container += (str(competi['uuid']) + ", ")

                    competitors_str = competitors_container.rstrip(", ")



                # 项目详情表
                project_data = result_data['project']
                if project_data is not None:
                    project_item = InvestProjectItem()

                    project_item['competitors'] = competitors_str
                    project_item['area'] = project_data['area']
                    project_item['company_uuid'] = project_data['company_uuid']
                    project_item['legal_person'] = project_data['legal_person']
                    project_item['website'] = project_data['website']
                    project_item['registered_address'] = project_data['registered_address']
                    project_item['uuid'] = project_data['uuid']
                    project_item['uscc'] = project_data['uscc']
                    project_item['industry'] = project_data['industry']
                    project_item['project_brief'] = project_data['project_brief']
                    project_item['project_name'] = project_data['project_name']
                    project_item['registered_capital'] = project_data['registered_capital']

                    if -1 == str(project_data['registered_capital']).find(r'人民币'):
                        project_item['currency_type'] = 2
                    else:
                        project_item['currency_type'] = 1

                    # project_item['registered_capital'] = re.sub(r'\D', '', str(project_data['registered_capital']))

                    re_match_data = re.search(r'\d+\.?\d*', str(project_data['registered_capital'])).group()
                    project_item['registered_capital'] = str(re_match_data)

                    project_item['project_desc'] = project_data['project_desc']

                    # tags
                    tags_list = []
                    if len(project_data['tags']) > 0:
                        for tags_item in project_data['tags']:
                            tags_list.append(tags_item['name'])

                    project_item['tags'] = ",".join(tags_list)

                    project_item['round'] = project_data['round']
                    project_item['company_name'] = project_data['company_name']
                    project_item['logo'] = project_data['project_img_url']
                    project_item['setup_date'] = project_data['setup_date']

                    yield project_item


                    # 核心人物表
                    core_people = project_data['projectCoreMembers']
                    if core_people is not None and len(core_people) > 0:
                        for c_people in core_people:
                            core_people_item = InvestCoreMemberItem()

                            core_people_item['uuid'] = project_data['uuid']
                            core_people_item['name'] = c_people['name']
                            core_people_item['position'] = c_people['position']
                            core_people_item['introduction'] = c_people['introduction']

                            yield core_people_item


                    # 项目融资明细表
                    project_finance_data = project_data['projectFinancings']
                    if project_finance_data is not None and len(project_finance_data) > 0:
                        for finance_data in project_finance_data:
                            finance_item = InvestFinanceRecordItem()

                            finance_item['uuid'] = project_data['uuid']
                            finance_item['put_date'] = finance_data['date']
                            finance_item['amount'] = finance_data['amount']
                            finance_item['round'] = finance_data['round']
                            # 投资人或机构 多个用逗号隔开
                            finance_item['investors'] = ""
                            finance_item['investors_uuid'] = ""
                            finance_item['investors_type'] = ""
                            use_investors = []
                            use_uuid = []
                            use_investors_type = []
                            if finance_data['investors'] is not None and len(finance_data['investors']) > 0:
                                for investor in finance_data['investors']:
                                    use_investors.append(str(investor['investor']))
                                    use_investors_type.append(str(investor['investor_type']))
                                    if '' != investor['investor_uuid']:
                                        use_uuid.append(str(investor['investor_uuid']))

                                finance_item['investors'] = ",".join(use_investors)
                                finance_item['investors_uuid'] = ",".join(use_uuid)
                                finance_item['investors_type'] = ",".join(use_investors_type)

                            yield finance_item

            else:
                self.logger.warning("peng. these is no content")

















