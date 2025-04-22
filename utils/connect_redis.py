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
            password=None if self.config['password'] == 'None' else self.config['password'],
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

    def set_data(self, key, value, expire=None):
        """
        存储数据到Redis
        :param key: 键名
        :param value: 值
        :param expire: 过期时间(秒)，可选
        :return: bool 是否成功
        """
        try:
            if expire:
                self.redis_conn.setex(key, expire, value)
            else:
                self.redis_conn.set(key, value)
            return True
        except RedisError as e:
            print(f"存储数据失败: {e}")
            return False

    def get_data(self, key):
        """
        从Redis获取数据
        :param key: 键名
        :return: 值或None
        """
        try:
            value = self.redis_conn.get(key)
            return value
        except RedisError as e:
            print(f"获取数据失败: {e}")
            return None

    def close(self):
        """释放连接池资源"""
        try:
            self.pool.disconnect()
            print("Redis连接池已关闭")
        except RedisError as e:
            print(f"关闭连接池失败: {e}")

    # 支持with语句
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 使用示例
if __name__ == "__main__":
    # 配置参数
    redis_config = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None,
        'max_connections': 5
    }

    # 方式1：常规使用
    redis_mgr = RedisPoolManager()

    # 存储数据
    redis_mgr.set_data("username", "admin")
    redis_mgr.set_data("session_token", "abc123xyz456", expire=3600)  # 1小时后过期

    # 查询数据
    print("username:", redis_mgr.get_data("username"))
    print("session_token:", redis_mgr.get_data("session_token"))
    print("non_existent_key:", redis_mgr.get_data("non_existent_key"))

    # 关闭连接
    redis_mgr.close()

    # 方式2：使用with语句自动管理资源
    with RedisPoolManager() as mgr:
        mgr.set_data("temp_key", "temp_value")
        print("temp_key:", mgr.get_data("temp_key"))
    # with块结束后自动调用close()

    # 更多数据结构操作示例
    with RedisPoolManager() as mgr:
        # Hash操作
        mgr.redis_conn.hset("user:1001", "name", "李四")
        mgr.redis_conn.hset("user:1001", "age", 28)
        print("用户信息:", mgr.redis_conn.hgetall("user:1001"))

        # List操作
        mgr.redis_conn.lpush("messages", "hello")
        mgr.redis_conn.rpush("messages", "world")
        print("消息列表:", mgr.redis_conn.lrange("messages", 0, -1))

        # Set操作
        mgr.redis_conn.sadd("tags", "python", "redis", "database")
        print("标签集合:", mgr.redis_conn.smembers("tags"))
