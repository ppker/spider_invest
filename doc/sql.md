```sql

create table if not exists `invest_project_all_list` (
  `id` int(11) unsigned not null auto_increment,
  `project_name` varchar(64) NOT NULL DEFAULT '' COMMENT '项目名称',
  `brief` varchar(256) NOT NULL DEFAULT '' COMMENT '概要描述业务',
  `finance_amount` varchar(64) NOT NULL DEFAULT '' COMMENT '最近融资金额的数据',
  `industry` varchar(32) NOT NULL DEFAULT '' COMMENT '所属行业',
  `investors` varchar(256) NOT NULL DEFAULT '' COMMENT '最近一轮的投资者,多个使用逗号分隔',
  `uuid` char(32) not null default '' comment 'uuid，识别使用, 关联profile',
  `round` varchar(64) NOT NULL DEFAULT '' COMMENT '融资信息-轮',
  `logo` varchar(512) not null default '' comment '项目icon-logo图片地址, 后期下载到自己的图片服务器上面',
  `finance_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '最近一次融资日期',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  primary key (`id`) using btree,
  key `uuid_i` (`uuid`) using btree,
  key `project_name_i` (`project_name`) using btree,
  key `finance_date_i` (`finance_date`) using btree,
  key `industry_i` (`industry`) using btree
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 comment '项目all表概览信息list表';



create table if not exists `invest_project_news_List` (
  `id` bigint(20) unsigned not null auto_increment,
  `project_name` varchar(64) NOT NULL DEFAULT '' COMMENT '项目名称',
  `publish_time` date NOT NULL DEFAULT '1970-01-01' COMMENT '文章发布日期',
  `bundle_key` char(32) not null default '' comment 'bundle_key 绑定的key, 关联文章页面内容查询',
  `source` varchar(64) NOT NULL DEFAULT '' COMMENT '文章报告来源',
  `title` varchar(128) not null default '' comment '文章报告标题',
  `type` tinyint(2) unsigned not null default 3 comment '文章类型',
  `uuid` char(32) not null default '' comment 'uuid，识别使用, 关联各表',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  primary key (`id`) using btree,
  key `publish_time_i` (`publish_time`) using btree,
  key `bundle_key_i` (`bundle_key`) using btree,
  key `uuid_i` (`uuid`) using btree
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 comment '项目文章报告表';



create table if not exists `invest_project_profile` (
  `id` int(11) unsigned not null auto_increment,
  `competitors` text not null comment '参考的竞品，后期我们自己算法识别，或专门增加一张单表维护。目前暂仅取部分逗号分隔',
  `area` varchar(16) NOT NULL DEFAULT '' COMMENT '项目所属地',
  `company_uuid` char(32) not null default '' comment 'company_uuid 绑定公司的ic工商信息',
  `legal_person` varchar(32) not null default '' comment '法人代表',
  `website` varchar(128) not null default '' comment '公司官网',
  `registered_address` varchar(256) not null default '' comment '公司注册地址',
  `uuid` char(32) not null default '' comment 'uuid，识别使用, 关联各表',
  `uscc` char(18) not null default '' comment '信用代码',
  `industry` varchar(32) NOT NULL DEFAULT '' COMMENT '所属行业',
  `project_brief` varchar(256) NOT NULL DEFAULT '' COMMENT '简要描述业务',
  `project_name` varchar(64) NOT NULL DEFAULT '' COMMENT '项目名称',
  `registered_capital` decimal(12,0) not null default 0 comment '注册资本(万)',
  `currency_type` tinyint(2) unsigned not null default 1 comment '1 => 人民币, 2 => 美元',
  `project_desc` text not null comment '项目介绍',
  `tags` varchar(512) not null default '' comment '项目标签，多个标签逗号分隔',
  `round` varchar(32) not null default '' comment '当前融资轮数',
  `company_name` varchar(64) not null default '' comment '公司名字',
  `logo` varchar(512) not null default '' comment '项目logo, 后期存到自己的图片服务器',
  `setup_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '成立时间',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  primary key (`id`) using btree,
  key `company_uuid_i` (`company_uuid`) using btree,
  key `uuid_i` (`uuid`) using btree,
  key `project_name_i` (`project_name`) using btree,
  key `setup_date_d` (`setup_date`, `updated_at`) using btree
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 comment '项目明细表';


--- 工商信息表
create table if not exists `invest_business_ic_info` (
  `id` int(11) unsigned not null auto_increment,
  `company_type` varchar(64) not null default '' comment '企业类型',
  `registration_authority` varchar(128) not null default '登机机关',
  `approval_date` date not null default '1970-01-01' comment '核准日期',
  `legal_person` varchar(64) not null default '' comment '法人代表',
  `registered_address` varchar(256) not null default '' comment '公司注册地址',
  `business_term` varchar(256) not null default '' comment '营业期限',
  `uscc` char(18) not null default '' comment '统一社会信用代码',
  `insurer_num` int(10) unsigned not null default 0 comment '参保人员',
  `industry` varchar(32) NOT NULL DEFAULT '' COMMENT '所属行业',
  `company_name_used` varchar(128) not null default '' comment '曾用名',
  `registration_num` char(15) not null default '' comment '工商注册号',
  `registered_capital` decimal(12,0) not null default 0 comment '注册资本(万)',
  `currency_type` tinyint(2) unsigned not null default 1 comment '1 => 人民币, 2 => 美元',
  `operating_scope` text not null comment '经营范围',
  `uuid` char(32) not null default '' comment 'uuid，识别使用, 关联各表',
  `operating_state` varchar(64) not null default '' comment '登记状态',
  `contributed_capital` decimal(12,0) not null default 0 comment '已缴资本(万)',
  `company_name` varchar(64) not null default '' comment '公司名字',
  `setup_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '成立时间',
  `company_url` varchar(512) not null default '' comment '公司网址，目前是企查查的链接',
  `company_name_en` varchar(64) not null default '' comment '英文名',
  `org_code` varchar(32) not null default '' comment '组织机构代码',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  primary key (`id`) using btree,
  key `uuid_i` (`uuid`) using btree,
  key `setup_date_i` (`setup_date`) using btree,
  key `updated_at_i` (`updated_at`) using btree
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 comment '工商信息详情表';







--- 股东表
create table if not exists `invest_holder_stock` (
  `id` bigint(20) unsigned not null auto_increment,
  `capital_contribution` decimal(12, 0) not null default 0 comment '认缴出资额(万)',
  `name` varchar(128) not null default '' comment '股东姓名',
  `shareholder_type` varchar(32) not null default '' comment '股东类型',
  `date_contribution` date NOT NULL DEFAULT '1970-01-01' COMMENT '认缴日期',
  `ratio` varchar(16) not null default '' comment '持股比例',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  primary key (`id`) using btree,
  key `date_contribution_i` (`date_contribution`) using btree
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 comment '股东明细记录表';







create table if not exists `invest_project_core_member` (
  `id` bigint(20) unsigned not null auto_increment,
  `uuid` char(32) not null default '' comment 'uuid，识别使用, 关联各表',
  `name` varchar(128) not null default '' comment '核心人物姓名',
  `position` varchar(32) not null default '' comment '职位',
  `introduction` text not null comment '人物背景介绍',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  primary key (`id`) using btree,
  key `uuid_i` (`uuid`) using btree
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 comment '项目核心人物表';


create table if not exists `invest_finance_record` (
  `id` bigint(20) unsigned not null auto_increment,
  `uuid` char(32) not null default '' comment 'uuid，识别使用, 关联各表',
  `put_date` date NOT NULL DEFAULT '1970-01-01' COMMENT '融资日期',
  `amount` varchar(64) not null default '' comment '融资金额',
  `round` varchar(32) not null default '' comment '融资轮数',
  `investors` varchar(256) not null default '' comment '投资人或机构，多个用逗号分隔',
  `investors_uuid` text not null comment '投资人和机构对于的uuid, 用户后续查询机构信息使用，跟investors保持一一对应',
  `investors_type` varchar(128) not null default '' comment '投资人/机构类型，跟investors保持一一对应, 0 => 未知, 1 => 个人, 2 => 机构',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  primary key (`id`) using btree,
  key `uuid_i` (`uuid`) using btree,
  key `put_date_i` (`put_date`) using btree
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 comment '项目融资明细表';

```