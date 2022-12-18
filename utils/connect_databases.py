# -*- coding:utf-8 -*-
# Author: Min
# Date  : 2022/7/27 16:45
# Desc  : 数据库连接工具

class CustomStdout:
    def __init__(self, appRootDir, cmd, recode):
        import sys, datetime, os
        self.console = sys.stdout
        sys.stdout = self
        # sys.stderr = self
        self.appRootDir = appRootDir + 'logs'
        self.procFlag = "%s_%s_%d" % (cmd, datetime.datetime.strftime(datetime.datetime.now(), '%H%M%S'), os.getpid())
        self.recode = recode

    def write(self, outStr):
        try:
            self.console.write(outStr)
        except:
            import traceback
            traceback.print_exc()
        finally:
            self.writeFile(outStr)

    def flush(self):
        pass

    def writeFile(self, outStr):
        if self.recode == 0: return
        try:
            import datetime, os
            dir_path = self.appRootDir + '/' + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d') + '/'
            if not os.path.exists(dir_path): os.makedirs(dir_path)
            file_path = dir_path + self.procFlag + '.log'
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(outStr)
        except:
            pass


# 加载配置
def load_config(project_name, cmd):
    import os
    import sys
    import configparser

    # project_name = 'erp-phds-data-middle'
    appRootDir = None
    if getattr(sys, 'frozen', False):
        appRootDir = os.path.dirname(sys.executable)
    elif __file__:
        appRootDir = os.path.dirname(__file__)
    if appRootDir is None:
        print('程序运行路径异常,退出程序')
        os._exit(-1)

    if project_name in appRootDir:
        index = appRootDir.find(project_name)
        appRootDir = appRootDir[0:index + len(project_name)]
    if appRootDir.endswith('/') is False:
        appRootDir = appRootDir + '/'
    appRootDir = appRootDir.replace('\\', '/')

    print("应用(%s) 根目录路径: %s" % (project_name, appRootDir))

    configList = []
    for file in os.listdir(appRootDir):
        file_path = appRootDir + file
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1] == '.ini':
            configList.append(file_path)

    config = configparser.RawConfigParser()
    config.read(filenames=configList, encoding='utf8')
    recode = config.getint('log', 'recode')
    CustomStdout(appRootDir, cmd, recode)
    return appRootDir, config


_db_mng_map = {}


def load_database_config(config):
    from utils.class_define import DatabaseClearThread, DatabaseManagerBean
    db_clear_thread = DatabaseClearThread()
    for session in config.sections():
        if session.startswith('dbload::'):
            mngName = session.replace('dbload::', '', 1)
            _db_mng_map[mngName] = DatabaseManagerBean(config.get(session, 'dbtype'),
                                                       config.get(session, 'host'),
                                                       config.get(session, 'port'),
                                                       config.get(session, 'username'),
                                                       config.get(session, 'password'),
                                                       config.get(session, 'database'),
                                                       db_clear_thread)
            print("加载数据库管理 %s,%s" % (mngName, str(_db_mng_map[mngName])))


def getDatabaseOperation(databaseName):
    mng = _db_mng_map.get(databaseName, None)
    if mng is None: raise ValueError("找不到指定数据库对象:%s" % databaseName)
    return mng
