# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2025-04-22
# Desc  :
import configparser
import os
from pathlib import Path

import redis
from redis.exceptions import RedisError


class RedisConfigManager:
    """Redis配置管理器"""

    @classmethod
    def load_config(cls, config_file=None):
        """
        加载Redis配置
        优先从指定配置文件读取，其次从环境变量读取，最后使用默认值
        """
        # 默认配置
        config = {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'password': None,
            'max_connections': 10
        }

        # 尝试从配置文件读取
        if config_file is None:
            # 尝试查找默认配置文件位置
            possible_locations = [
                'config.ini',
                str(Path.home() / 'config.ini'),
                '/etc/redis_config.ini'
            ]

            for location in possible_locations:
                if os.path.exists(location):
                    config_file = location
                    break

        if config_file and os.path.exists(config_file):
            try:
                parser = configparser.ConfigParser()
                parser.read(config_file)

                if 'redis' in parser:
                    redis_section = parser['redis']
                    config.update({
                        'host': redis_section.get('host', config['host']),
                        'port': redis_section.getint('port', config['port']),
                        'db': redis_section.getint('db', config['db']),
                        'password': redis_section.get('password', config['password']),
                        'max_connections': redis_section.getint('max_connections', config['max_connections'])
                    })
            except Exception as e:
                print(f"读取配置文件失败，使用默认配置: {e}")

        # 环境变量覆盖配置 (可选)
        config.update({
            'host': os.getenv('REDIS_HOST', config['host']),
            'port': int(os.getenv('REDIS_PORT', config['port'])),
            'db': int(os.getenv('REDIS_DB', config['db'])),
            'password': os.getenv('REDIS_PASSWORD', config['password']),
            'max_connections': int(os.getenv('REDIS_MAX_CONNECTIONS', config['max_connections']))
        })

        return config


class RedisPoolManager:
    def __init__(self, config_file=None):
        """
        初始化Redis连接池
        :param config_file: 可选，指定配置文件路径
        """
        # 加载配置
        self.config = RedisConfigManager.load_config(config_file)

        # 创建连接池
        self.pool = redis.ConnectionPool(
            host=self.config['host'],
            port=self.config['port'],
            db=self.config['db'],
            password=self.config['password'],
            max_connections=self.config['max_connections'],
            decode_responses=True,
            health_check_interval=30
        )
        self.redis_conn = redis.Redis(connection_pool=self.pool)

        # 测试连接
        try:
            self.redis_conn.ping()
            print(f"成功连接到Redis服务器: {self.config['host']}:{self.config['port']}")
        except RedisError as e:
            print(f"Redis连接失败: {e}")
            raise


if __name__ == "__main__":
    # 方式1：使用配置文件（自动查找）
    redis_mgr1 = RedisPoolManager()

    # 方式2：指定配置文件路径
    redis_mgr2 = RedisPoolManager(config_file='/path/to/your_config.ini')

    # 方式3：完全从环境变量读取
    # 需要先设置环境变量
    os.environ['REDIS_HOST'] = '127.0.0.1'
    os.environ['REDIS_PORT'] = '6379'
    redis_mgr3 = RedisPoolManager()  # 环境变量方案

    # 使用示例
    with redis_mgr1:
        redis_mgr1.set_data("config_test", "from_config_file")
        print(redis_mgr1.get_data("config_test"))
