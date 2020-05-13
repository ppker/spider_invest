#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time     : 2020/5/10
# @Author   : Peng
# @Desc


import scrapy, json
from urllib import parse
from scrapy.http import FormRequest
from invest.items import InvestItem

class CtpSpider(scrapy.Spider):

    name = 'chuangtoupai'
    allowed_domains = ['primary-market.aigauss.com']

    use_page = 1

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "LOG_ENABLED": True,
        "COOKIES_ENABLES": False,

        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 'invest.middlewares.RotateUserAgentMiddleware': 400,
        },
        "FEED_EXPORT_ENCODING": 'utf-8', # feed export 导出json文件 中文不乱码
    }
    url_data = {
        "is_overseas": "0",
        "page": str(use_page),
        "size": "20",
        "industries": "",
        "phases": "",
        "areas": "",
        "time": "0",
        "first_page_timestamp": "2020-5-10 14:38:29"
    }

    common_headers = {
        ":method": "GET",
        ":path": "/primary-market-pro-v3/homepage/news_list?{}".format(parse.urlencode(url_data)),
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


    def start_requests(self):
        return [
            FormRequest(self.pre_url + "/primary-market-pro-v3/homepage/news_list", method="GET", headers=self.common_headers,
                        formdata=self.url_data, callback=self.list_parse, meta={"page": self.use_page}, dont_filter=False)
        ]

    def list_parse(self, response):
        if 200 == response.status:
            out_data = json.loads(response.body.decode('utf-8'))

            # self.logger.warning(">>>> %s", out_data)
            if 200 == out_data['status'] and ('result' in out_data and 0 < len(out_data['result']['data'])):
                list_data = out_data['result']['data']

                for v in list_data:
                    item = InvestItem()
                    item['project_name'] = v.get('project_name', '')
                    item['brief'] = v.get('brief', '')
                    item['finance_amount'] = v.get('finance_amount', '')
                    item['industry'] = v.get('industry', '')
                    item['investors'] = ",".join(v.get('investors', []))
                    item['uuid'] = v.get('uuid', '')
                    item['round'] = v.get('round', '')
                    item['company_name'] = v.get('company_name', '')
                    item['project_img_url'] = v.get('project_img_url', '')
                    yield item

                # 获取下一页的数据

                # if True == out_data['result']['has_more'] and 2 > int(out_data['result']['current_page']):
                if True == out_data['result']['has_more']:
                    now_page_num = int(out_data['result']['current_page']) + 1

                    self.url_data['page'] = str(now_page_num)
                    self.use_page = now_page_num
                    self.logger.warning(">>>>>>>>>>>> 开始第%d页", now_page_num)
                    yield FormRequest(self.pre_url + "/primary-market-pro-v3/homepage/news_list", method="GET", headers=self.common_headers,
                        formdata=self.url_data, callback=self.list_parse, meta={"page": self.use_page}, dont_filter=False)


        else:
            self.logger.warning("peng. there is no content")







