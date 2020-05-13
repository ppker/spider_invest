- 申请验证码
```
https://primary-market.aigauss.com/primary-market-pro-v3/account/send_confirm_code
{
	"mobile": "18521568316"
}	
	
```

- 登录
```
https://primary-market.aigauss.com/primary-market-pro-v3/account/login
{
	"confirmCode": "7212",
	"mobile": "18521568316"
}

```

- 顶部开头4个大类
```
https://primary-market.aigauss.com/primary-market-pro-v3/homepage/homepage_config


{
	"result": {
		"businessStoreConfigList": [{
			"icon": "http://ipo-oss.aigauss.com/news_image/3561/47a853a0f46fb864ccac205c449d3561_108x108.png",
			"name": "项目库",
			"routerUrl": "homeProjectStore"
		}, {
			"icon": "http://ipo-oss.aigauss.com/news_image/0c55/9952853e8416022673e8531a0a600c55_108x108.png",
			"name": "项目专辑",
			"routerUrl": "homeBillboard"
		}, {
			"icon": "http://ipo-oss.aigauss.com/news_image/b3ca/7327dec08055899129fd95790fc4b3ca_108x108.png",
			"name": "机构库",
			"routerUrl": "homeOrgStore"
		}, {
			"icon": "http://ipo-oss.aigauss.com/news_image/bd95/c6620a83c74b0d2a6f73296cb029bd95_108x108.png",
			"name": "研报库",
			"routerUrl": "homeResearchReport"
		}],
		"background": "http://ipo-oss.aigauss.com/pm_images/9304/4362611b3830e8ee312922ea23ed9304.png"
	},
	"statusText": "success",
	"status": 200
}

```

- 行业趋势
```
https://primary-market.aigauss.com/primary-market-pro-v3/homepage/industry_trend?period_code=3

{
	"result": {
		"data": [{
			"projectCount": 29,
			"tradeSum": "356.7亿",
			"increaseAmount": 31.0,
			"name": "汽车交通",
			"eventCount": 31,
			"id": 13,
			"orgCount": 79
		}, {
			"projectCount": 132,
			"tradeSum": "322.5亿",
			"increaseAmount": 133.0,
			"name": "医疗健康",
			"eventCount": 133,
			"id": 8,
			"orgCount": 363
		}, {
			"projectCount": 29,
			"tradeSum": "313.2亿",
			"increaseAmount": 29.0,
			"name": "文娱传媒",
			"eventCount": 29,
			"id": 4,
			"orgCount": 53
		}, {
			"projectCount": 146,
			"tradeSum": "266.7亿",
			"increaseAmount": 147.0,
			"name": "企业服务",
			"eventCount": 147,
			"id": 9,
			"orgCount": 315
		}, {
			"projectCount": 13,
			"tradeSum": "242.7亿",
			"increaseAmount": 14.0,
			"name": "房产家居",
			"eventCount": 14,
			"id": 11,
			"orgCount": 41
		}],
		"total_count": 5,
		"total_page": 1,
		"has_more": false,
		"current_page": 1
	},
	"statusText": "success",
	"status": 200
}


```

- app 顶部的banner
```
https://primary-market.aigauss.com/primary-market-pro-v3/homepage/banner
{
	"result": {
		"data": [{
			"activityMode": "",
			"picUrl": "http://ipo-oss.aigauss.com/news_image/6755/96871256a153863a64c3ed93dcbe6755_1125x510.png",
			"routerUrl": "",
			"loginMode": "0"
		}],
		"total_count": 0,
		"total_page": 0,
		"has_more": false,
		"current_page": 0
	},
	"statusText": "success",
	"status": 200
}

```

- project profile 项目详细信息
```
https://primary-market.aigauss.com/primary-market-pro-v3/project_info/query/v4?uuid=d7c9b3bef17844659e21cadede5d1b47

uuid d7c9b3bef17844659e21cadede5d1b47


```

- list of project 项目列表
```
https://primary-market.aigauss.com/primary-market-pro-v3/homepage/news_list?is_overseas=0&page=1&size=15&industries=&phases=&areas=&time=0&first_page_timestamp=2020-5-10%2014%3A38%3A29

```

- ic_info 工商信息
```
https://primary-market.aigauss.com/primary-market-pro-v3/ic_info/query?uuid=facdfc74157c11ea9d8d8f0be39e7693
```

- all_project 项目库搜索
```
https://primary-market.aigauss.com/primary-market-pro-v3/project_info/list?order_by=2&industries=&phases=ANGEL&areas=%E5%8C%97%E4%BA%AC&finance_date_from=2020-02-12&page=1&size=15

```