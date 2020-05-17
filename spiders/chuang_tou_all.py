#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time     : 2020/5/11
# @Author   : Peng
# @Desc


import scrapy, json
from urllib import parse
from scrapy.http import FormRequest
from invest.items import InvestAllListItem

class CtpSpider(scrapy.Spider):

    # https://primary-market.aigauss.com/primary-market-pro-v3/project_info/list?order_by=1&industries=1%2C2%2C3%2C4&phases=ANGEL%2CPRE_A%2CA&areas=%E5%8C%97%E4%BA%AC&finance_date_from=2020-02-12&page=1&size=15
    name = 'chuangtouall'
    allowed_domains = ['primary-market.aigauss.com']

    use_page = 1

    custom_settings = {
        "DOWNLOAD_DELAY": 1.8,
        "LOG_ENABLED": True,
        "COOKIES_ENABLES": False,
        "CONCURRENT_REQUESTS": 8,

        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 'invest.middlewares.RotateUserAgentMiddleware': 400,
        },
        "FEED_EXPORT_ENCODING": 'utf-8', # feed export 导出json文件 中文不乱码
    }
    url_data = {
        "order_by": "1",
        "industries": "1,2,3,4",
        "phases": "ANGEL,PRE_A,A",
        "areas": "北京",
        "finance_date_from": "2019-05-12",
        "page": str(use_page),
        "size": "15",
    }

    common_headers = {
        ":method": "GET",
        ":path": "/primary-market-pro-v3/project_info/list?{}".format(parse.urlencode(url_data)),
        # ":path": "/primary-market-pro-v3/homepage/news_list?is_overseas=0&page=1&size=15&industries=&phases=&areas=&time=0&first_page_timestamp=2020-5-10%2014%3A38%3A29",
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

    pre_url = "https://primary-market.aigauss.com"

    common_industries = {}
    common_phases = {}
    common_finance_date_from = {}
    common_areas = {}



    def start_requests(self):

        # 串行模式 先爬取公共数据然后再续爬虫业务流程
        use_data_common = self.common_headers
        use_data_common[':path'] = "/primary-market-pro-v3/pm_filter/get_filters?{}".format(parse.urlencode({"page_type": "2"}))
        return [
            # https://primary-market.aigauss.com/primary-market-pro-v3/pm_filter/get_filters?page_type=2
            FormRequest(self.pre_url + "/primary-market-pro-v3/pm_filter/get_filters", method="GET", headers=use_data_common,
                        formdata={"page_type": "2"}, callback=self.parse_common_data, dont_filter=True)
        ]


    def parse_common_data(self, response):
        if 200 == response.status:
            out_data = json.loads(response.body.decode('utf-8'))
            if 200 == out_data['status'] and ('result' in out_data and 0 < len(out_data['result']['data'])):
                for vv in out_data['result']['data']:
                    if 'industries' == vv['code']:
                        self.common_industries = vv['values']
                    elif 'phases' == vv['code']:
                        self.common_phases = vv['values']
                    elif 'finance_date_from' == vv['code']:
                        self.common_finance_date_from = vv['values']
                    elif 'areas' == vv['code']:
                        self.common_areas = vv['values']

                '''
                print(self.common_industries, self.common_phases, self.common_finance_date_from, self.common_areas)
                return
                '''

            # 进行业务筛选条件遍历
            use_condition = {
                "order_by": "1",
                "industries": "1,2,3,4",
                "phases": "ANGEL,PRE_A,A",
                "areas": "北京",
                "finance_date_from": "1991-03-16",
                "page": "1",
                "size": "15",
            }

            all_list_headers = self.common_headers

            for industries in self.common_industries:
                for phases in self.common_phases:
                    for areas in self.common_areas:
                        use_condition['industries'] = industries['code']
                        use_condition['phases'] = phases['code']
                        use_condition['areas'] = areas['code']

                        all_list_headers[':path'] = "/primary-market-pro-v3/project_info/list?{}".format(parse.urlencode(use_condition))
                        # 爬虫请求
                        # print(">>>>>>>>>>", use_condition)
                        # print(">>>>>>>>>>", all_list_headers)
                        yield FormRequest(self.pre_url + "/primary-market-pro-v3/project_info/list", method="GET", headers=all_list_headers,
                                    formdata=use_condition, callback=self.list_parse, meta={'last_condition': use_condition}, dont_filter=False)





    def list_parse(self, response):
        if 200 == response.status:
            out_data = json.loads(response.body.decode('utf-8'))

            # self.logger.warning(">>>> %s", out_data)
            if 200 == out_data['status']:
                tem_str = response.meta['last_condition']
                print("数据集是---%s----%s----%s" % (out_data['result']['data'], tem_str, response.url))

            if 200 == out_data['status'] and ('result' in out_data and 0 < len(out_data['result']['data'])):
                list_data = out_data['result']['data']

                for v in list_data:
                    item = InvestAllListItem()
                    item['project_name'] = v.get('name', '')
                    item['brief'] = v.get('brief', '')
                    item['finance_amount'] = v.get('finance_amount', '')
                    item['industry'] = v.get('industry', '')
                    item['investors'] = ",".join(v.get('investors', []))
                    item['uuid'] = v.get('uuid', '')
                    item['round'] = v.get('round', '')
                    item['logo'] = v.get('logo', '')
                    if '-' == v.get('finance_date') or '' == v.get('finance_date', ''):
                        item['finance_date'] = "1970-01-01"
                    else:
                        item['finance_date'] = v.get('finance_date', '')

                    yield item

                # 是否出现全量遗漏
                if out_data['result']['total_count'] > 510:
                    self.logger.warning(">>>>>>>>>>>peng. 发现数据遗漏情况 %d---%s", out_data['result']['total_count'], response.meta['last_condition'])
                    print(">>>>>>>>>>>peng. 发现数据遗漏情况 %d---%s" % (out_data['result']['total_count'], response.meta['last_condition']))

                # 获取下一页的数据

                # if True == out_data['result']['has_more'] and 2 > int(out_data['result']['current_page']):
                if True == out_data['result']['has_more']:
                    now_page_num = int(out_data['result']['current_page']) + 1

                    last_condition = response.meta['last_condition']
                    last_condition['page'] = str(now_page_num)

                    self.logger.warning(">>>>>>>>>>>> 开始第%d页", now_page_num)
                    print(">>>>>>>>>>>> 开始第%d页" % (now_page_num,))
                    # 构造请求头
                    page_list_headers = self.common_headers
                    page_list_headers[':path'] = "/primary-market-pro-v3/project_info/list?{}".format(parse.urlencode(last_condition))

                    yield FormRequest(self.pre_url + "/primary-market-pro-v3/project_info/list",
                                      method="GET", headers=page_list_headers,
                                      formdata=last_condition, callback=self.list_parse,
                                      meta={'last_condition': last_condition}, dont_filter=False)



        else:
            self.logger.warning("peng. there is no content")


