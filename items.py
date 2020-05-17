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


class InvestNewsListItem(scrapy.Item):

    project_name = scrapy.Field()
    publish_time = scrapy.Field()
    bundle_key = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    uuid = scrapy.Field()


    def get_insert_sql(self):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        insert_sql = '''
            insert into `invest_project_news_List`(project_name, publish_time, bundle_key, source, title, type, uuid, created_at, updated_at) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        params = (
            self['project_name'],
            self['publish_time'],
            self['bundle_key'],
            self['source'],
            self['title'],
            self['type'],
            self['uuid'],
            str(now_time),
            str(now_time)
        )

        return insert_sql, params



class InvestProjectItem(scrapy.Item):

    competitors = scrapy.Field()
    area = scrapy.Field()
    company_uuid = scrapy.Field()
    legal_person = scrapy.Field()
    website = scrapy.Field()
    registered_address = scrapy.Field()
    uuid = scrapy.Field()
    uscc = scrapy.Field()
    industry = scrapy.Field()
    project_brief = scrapy.Field()
    project_name = scrapy.Field()
    registered_capital = scrapy.Field()
    currency_type = scrapy.Field()
    project_desc = scrapy.Field()
    tags = scrapy.Field()
    round = scrapy.Field()
    company_name = scrapy.Field()
    logo = scrapy.Field()
    setup_date = scrapy.Field()


    def get_insert_sql(self):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        insert_sql = '''
            insert into `invest_project_profile`(competitors, area, company_uuid, legal_person, website, registered_address, 
            uuid, uscc, industry, project_brief, project_name, registered_capital, currency_type, project_desc, tags, round, company_name, 
            logo, setup_date, created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

        # vars()
        '''
        tem_params = vars(self).items().values()
        tem_params.extend([now_time, now_time])
        return insert_sql, tem_params
        '''
        params = (
            self['competitors'],
            self['area'],
            self['company_uuid'],
            self['legal_person'],
            self['website'],
            self['registered_address'],
            self['uuid'],
            self['uscc'],
            self['industry'],
            self['project_brief'],
            self['project_name'],
            self['registered_capital'],
            int(self['currency_type']),
            self['project_desc'],
            self['tags'],
            self['round'],
            self['company_name'],
            self['logo'],
            self['setup_date'],
            str(now_time),
            str(now_time),
        )
        return insert_sql, params



class InvestCoreMemberItem(scrapy.Item):

    uuid = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    introduction = scrapy.Field()


    def get_insert_sql(self):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        insert_sql = '''
            insert into `invest_project_core_member`(uuid, name, position, introduction, created_at, updated_at) values (%s, %s, %s, 
            %s, %s, %s);
        '''
        params = (
            self['uuid'],
            self['name'],
            self['position'],
            self['introduction'],
            str(now_time),
            str(now_time),
        )

        return insert_sql, params


class InvestFinanceRecordItem(scrapy.Item):

    uuid = scrapy.Field()
    put_date = scrapy.Field()
    amount = scrapy.Field()
    round = scrapy.Field()
    investors = scrapy.Field()
    investors_uuid = scrapy.Field()
    investors_type = scrapy.Field()

    def get_insert_sql(self):

        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        insert_sql = '''
            insert into `invest_finance_record`(uuid, put_date, amount, round, investors, investors_uuid, investors_type, 
            created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        params = (
            self['uuid'],
            self['put_date'],
            self['amount'],
            self['round'],
            self['investors'],
            self['investors_uuid'],
            self['investors_type'],
            str(now_time),
            str(now_time),
        )

        return insert_sql, params


class InvestShareHolderItem(scrapy.Item):

    capital_contribution = scrapy.Field()
    name = scrapy.Field()
    shareholder_type = scrapy.Field()
    date_contribution = scrapy.Field()
    ratio = scrapy.Field()

    def get_insert_sql(self):

        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        insert_sql = '''
            insert into `invest_holder_stock`(capital_contribution, name, shareholder_type, date_contribution, ratio, 
            created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s);
        '''
        params = (
            self['capital_contribution'],
            self['name'],
            self['shareholder_type'],
            self['date_contribution'],
            self['ratio'],
            str(now_time),
            str(now_time),
        )

        return insert_sql, params


class InvestBusinessIcItem(scrapy.Item):

    company_type = scrapy.Field()
    registration_authority = scrapy.Field()
    approval_date = scrapy.Field()
    legal_person = scrapy.Field()
    registered_address = scrapy.Field()
    business_term = scrapy.Field()
    uscc = scrapy.Field()
    insurer_num = scrapy.Field()
    industry = scrapy.Field()
    company_name_used = scrapy.Field()
    registration_num = scrapy.Field()
    registered_capital = scrapy.Field()
    currency_type = scrapy.Field()
    operating_scope = scrapy.Field()
    uuid = scrapy.Field()
    operating_state = scrapy.Field()
    contributed_capital = scrapy.Field()
    company_name = scrapy.Field()
    setup_date = scrapy.Field()
    company_url = scrapy.Field()
    company_name_en = scrapy.Field()
    org_code = scrapy.Field()


    def get_insert_sql(self):

        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        insert_sql = '''
            insert into `invest_business_ic_info`(company_type, registration_authority, approval_date, legal_person, registered_address, 
            business_term, uscc, insurer_num, industry, company_name_used, registration_num, registered_capital, currency_type, 
            operating_scope, uuid, operating_state, contributed_capital, company_name, setup_date, company_url, company_name_en, org_code, 
            created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

        params = (
            self['company_type'],
            self['registration_authority'],
            self['approval_date'],
            self['legal_person'],
            self['registered_address'],
            self['business_term'],
            self['uscc'],
            self['insurer_num'],
            self['industry'],
            self['company_name_used'],
            self['registration_num'],
            self['registered_capital'],
            self['currency_type'],
            self['operating_scope'],
            self['uuid'],
            self['operating_state'],
            self['contributed_capital'],
            self['company_name'],
            self['setup_date'],
            self['company_url'],
            self['company_name_en'],
            self['org_code'],
            str(now_time),
            str(now_time),
        )

        return insert_sql, params














