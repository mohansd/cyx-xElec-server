# -*- coding: utf-8 -*-
from apscheduler.jobstores.mongodb import MongoDBJobStore

DEBUG = True

# Token 配置
SECRET_KEY = 'GlodMountain'  # 加密
TOKEN_EXPIRATION = 30 * 24 * 3600  # 有效期: 30天

# MongoDB 数据库配置
MONGODB_SETTINGS = {
    'host': 'mongodb://wuyao:wuyao123@182.92.242.32:37018/GlodMountain',
    'connect': True
}
# Redis 数据库配置
REDIS_URL = "redis://127.0.0.1:6379/0"

SCHEDULER_API_ENABLED = True
# 持久化配置
SCHEDULER_JOBSTORES = {
    'default': MongoDBJobStore(database='GlodMountain', collection='apscheduler', host='182.92.242.32', port=37018,
                               username="wuyao", password="wuyao123", authMechanism='SCRAM-SHA-1',
                               authSource="GlodMountain")
}

SCHEDULER_EXECUTORS = {
    'default': {'type': 'threadpool', 'max_workers': 20}
}
