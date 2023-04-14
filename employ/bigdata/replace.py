# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2023/3/14
# Desc  : 替换字符

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("update_table").getOrCreate()

mysql_url = "jdbc:mysql://120.78.89.99:8836/bdcp_stg_troy"
mysql_properties = {
    "user": "root",
    "password": "bhds@ykyy1226!",
    "driver": "com.mysql.jdbc.Driver"
}
mysql_table = "tb_bsd_mcdrug_nmpa_split"

df = spark.read.jdbc(url=mysql_url, table=mysql_table, properties=mysql_properties)

df.show()

# df_cols = df.withColum("newSpec", regexp_replace("spec", "（", "("))
columns = df.columns()


# df_cols.show()

spark.stop()
