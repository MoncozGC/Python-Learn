# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/06/25
# Desc  : 配置文件解析

import os
from configparser import ConfigParser


def get_root_path():
    current_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return current_path


def load_config():
    conf = ConfigParser()
    # 可配置多个配置文件, 但是属性值不要重复
    conf.read([os.path.join(get_root_path(), "cnf/profile.ini"),
               os.path.join(get_root_path(), "cnf/dic.ini")],
              encoding="utf-8")
    # 使用一个配置文件进行测试环境和开发环境的切换
    profile = conf["application"]["profile_active"]
    if profile == "test":
        conf.read([os.path.join(get_root_path(), "cnf/config_test.ini")], encoding="utf-8")
    else:
        conf.read([os.path.join(get_root_path(), "cnf/config_dev.ini")], encoding="utf-8")
    CnfUtil.cnf = conf


class CnfUtil:
    cnf: ConfigParser = None


if __name__ == '__main__':
    # load_config()
    # conf = CnfUtil().cnf
    # print(conf['gds_dic'])
    # print(conf['gds_dic']['susx'])
    print(os.path.join(get_root_path()))
