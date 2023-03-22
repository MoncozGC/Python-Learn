# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2022/5/26 21:26
# Desc  :
from YKYY.PHDS.database.database_load import getDatabaseOperation


def init(cmd):
    # 加载配置文件
    from YKYY.PHDS.config.app_config import load_config
    # 文件夹名称
    appRootDir, config = load_config('Python-Employ', cmd)

    # 初始化数据库
    from YKYY.PHDS.database.database_load import load_database_config
    load_database_config(config)


if __name__ == '__main__':
    init('')

    higLvCode = 1800000000
    # QUERY_SQL = """SELECT COUNT(cfyCode)+1 FROM tb_base_classify WHERE cfyLevel = 6  AND higLvCode  = %s """ % higLvCode
    QUERY_SQL = """select a.wareid,warename,waresimname,warespec,a.wareunit,c.classname,prod_add,producer,fileno,barcode
    from u_ware_q a,u_ware_ext b ,v_ware_class c 
    where a.wareid=b.wareid and a.wareid=c.wareid and c.parentcode='03' """
    data = getDatabaseOperation("wcs").query(QUERY_SQL)
    print(data)
