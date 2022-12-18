# Project Engineering Description(项目工程描述)

```text
├──Employ工程
	├──BHDSWarehouse: YKYY数据仓库项目测试使用
	├──employ: 练习使用
	├──hpv: hpv九价购买
	├──monitor: Flink、YARN、Zabbix组件监控
	├──Participle: Jieba中文分词器使用
	├──PHDS: PHDS药店健康诊断系统测试使用
	├──reborn: 投胎模拟器
	├──reptile: 爬虫相关
	├──utils: 工具类使用
	├──WxChatRecordTool: 统计微信群聊天记录发言数以及制作聊天记录词云
```

### 配置信息
在根目录下配置config.ini文件, 基本的日志和数据库信息
```ini
# base config
[log]
outDirectory=./Logs
fileTimeFormat = %Y%m%d
timeFormat = %Y-%m-%d %H:%M:%S.%f
recode=0

# MYSQL PHDS-dev
[dbload::phds_base]
dbtype = mysql
host = xxxx
port = 3306
username = root
password = root
database = database

# CK PHDS-dev
[dbload::warehouse_phds]
dbtype = clickHouse
host = xxxx
port = 8235
username = default
password = default
database = database
```