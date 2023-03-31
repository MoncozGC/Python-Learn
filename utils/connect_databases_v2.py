# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/3/30 16:00
# Desc  : dataframe写入数据库
from sqlalchemy import create_engine


class DBConnCls:
    def __init__(self, conf):
        self.conf = conf
        self.engine = None

    # 建立和数据库系统的连接
    def connect(self):
        host = self.conf["mysql"]["host"]
        port = int(self.conf["mysql"]["port"])
        user = self.conf["mysql"]["user"]
        passwd = self.conf["mysql"]["password"]
        db = self.conf["mysql"]["database"]

        connection_string = f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}"
        self.engine = create_engine(connection_string)

    def write_df_to_sql(self, df, table_name, if_exists='replace', index=False, **kwargs):
        """
        将DataFrame写入数据库
        :param df: 数据集
        :param table_name: 写入的表名
        :param if_exists: replace 覆盖写入甚至会改变表字段; append为追加写入, 不会改变表字段, df的字段名需与表字段名一致
        :param index:
        :param kwargs:
        :return:
        """
        if self.engine is None:
            self.connect()
        df.to_sql(table_name, self.engine, if_exists=if_exists, index=index, **kwargs)
