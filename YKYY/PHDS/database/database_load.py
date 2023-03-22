
_db_mng_map = {}


def load_database_config(config):
    from YKYY.PHDS.database.class_define import DatabaseClearThread,DatabaseManagerBean
    db_clear_thread = DatabaseClearThread()
    # print('连接检测线程',db_clear_thread)
    for session in  config.sections():
        if session.startswith('dbload::'):
            mngName = session.replace('dbload::','',1)
            _db_mng_map[mngName] = DatabaseManagerBean(config.get(session, 'dbtype'),
                                                       config.get(session, 'host'),
                                                       config.get(session, 'port'),
                                                       config.get(session, 'username'),
                                                       config.get(session, 'password'),
                                                       config.get(session, 'database'),
                                                       db_clear_thread)
            print("加载数据库管理 %s,%s" % (mngName, str(_db_mng_map[mngName])))


def getDatabaseOperation(databaseName):
    mng = _db_mng_map.get(databaseName,None)
    if mng == None: raise ValueError("找不到指定数据库对象:%s" % databaseName)
    return mng

