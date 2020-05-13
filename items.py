# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy, time


class InvestItem(scrapy.Item):
    # define the fields for your item here like:
    project_name = scrapy.Field() # 项目名称 project_name
    brief = scrapy.Field() # 概要描述业务 brief
    finance_amount = scrapy.Field() # 最近融资金额的数据 finance_amount
    industry = scrapy.Field() # 所属行业 industry
    investors = scrapy.Field() # 最近一轮的投资者,多个使用逗号分隔 investors
    uuid = scrapy.Field() # uuid
    round = scrapy.Field() # 融资信息-轮 round
    company_name = scrapy.Field() # 公司名称 company_name
    project_img_url = scrapy.Field() # 项目icon-logo图片地址, 后期下载到自己的图片服务器上面 project_img_url


    def get_insert_sql(self):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        insert_sql = """
            insert into `invest_list_project`(project_name, brief, finance_amount, industry, investors, uuid, round, company_name, project_img_url, 
            created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        
        """
        params = (
            self['project_name'],
            self['brief'],
            self['finance_amount'],
            self['industry'],
            self['investors'],
            self['uuid'],
            self['round'],
            self['company_name'],
            self['project_img_url'],
            str(now_time),
            str(now_time),
        )

        return insert_sql, params


class InvestAllListItem(scrapy.Item):

    project_name = scrapy.Field()
    brief = scrapy.Field()
    finance_amount = scrapy.Field()
    industry = scrapy.Field()
    investors = scrapy.Field()
    uuid = scrapy.Field()
    round = scrapy.Field()
    logo = scrapy.Field()
    finance_date = scrapy.Field()


    def get_insert_sql(self):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        insert_sql = """
            insert into `invest_project_all_list`(project_name, brief, finance_amount, industry, investors, uuid, round, logo, 
            finance_date, created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            self['project_name'],
            self['brief'],
            self['finance_amount'],
            self['industry'],
            self['investors'],
            self['uuid'],
            self['round'],
            self['logo'],
            self['finance_date'],
            str(now_time),
            str(now_time),
        )

        return insert_sql, params