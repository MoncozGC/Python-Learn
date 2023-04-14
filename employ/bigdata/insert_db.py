# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/3/14 9:54
# Desc  : 查询A数据库数据字段写入B数据库中

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("update_table").getOrCreate()

# 从A表中读取数据
table_a = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://server01:3306/dev") \
    .option("user", "root") \
    .option("password", "hadoop") \
    .option("dbtable", "user") \
    .load()

# 从A表中查询需要更新的字段
# selected_cols = table_a.select(col("password"), col("username"))
repDF = table_a.withColumn("newSpec", regexp_replace("password", "（", "("), )

repDF.show()

# 将数据更新到B表
# selected_cols.write.format("jdbc") \
#     .option("url", "jdbc:mysql://server01:3306/dev") \
#     .option("user", "root") \
#     .option("password", "hadoop") \
#     .option("dbtable", "user_1") \
#     .option("truncate", "true") \
#     .mode("overwrite") \
#     .save()

spark.stop()
