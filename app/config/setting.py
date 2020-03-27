# _*_ coding: utf-8 _*_
"""
  Swagger 配置
"""
import os
from collections import namedtuple

VERSION = "0.1.0"  # 项目版本

# is_dev_mode = os.path.exists('app/config/dev_setting.py') # 'development' & 'product' (开发环境 or 生产环境)

is_dev_mode = True

EXTERNAL_URL = '182.92.242.32:8020'  # 外部（云服务器）地址
INTERNAL_URL = '0.0.0.0:8020'  # 内部（本地）地址
SERVER_URL = INTERNAL_URL if is_dev_mode else EXTERNAL_URL

EXTERNAL_SCHEMES = ["https", "http"]  # 外部（云服务器）支持 https 和 http 协议
INTERNAL_SCHEMES = ["http"]  # 内部只支持http
SERVER_SCHEMES = INTERNAL_SCHEMES if is_dev_mode else EXTERNAL_SCHEMES

SWAGGER_TAGS = []  # 在'/app/api/__init__.py'中create_blueprint_list设置
SWAGGER = {
    "swagger_version": "2.0",
    "info": {
        "title": "金峰项目: API文档",
        "version": VERSION,
        "description": "描述暂无",
        "contact": {
            "responsibleOrganization": "TaleCeres",
            "responsibleDeveloper": "董冬伟",
            "email": "bodanli159951@163.com",
            "url": "http://51anquan.com"
        },
        "termsOfService": "http://51anquan.com"
    },
    "host": SERVER_URL,  # "api.ivinetrue.com",
    "basePath": "/",  # base bash for blueprint registration
    "tags": SWAGGER_TAGS,  # 在'/app/api/v1/__init__.py'定义
    "schemes": SERVER_SCHEMES,
    "operationId": "getmyData",
    "securityDefinitions": {
        'basicAuth': {
            'type': 'basic'
        }
    }
}

# SWAGGER的安全访问方式
specs_security = [
    {
        "basicAuth": []
    }
]

# all api by module(version)
# 可以控制Swagger API文档的显示顺序
ALL_RP_API_LIST= \
    ['cms.admin', 'cms.group', 'cms.auth',
     'cms.user', 'cms.cdkey', 'cms.agent', 'cms.company',
     'cms.project', 'cms.device_category', 'cms.device'] +\
    ['v1.token', 'v1.user', 'v1.cdkey', 'v1.device', 'v1.project', 'v1.alarm', 'v1.device', 'v1.job', 'v1.statement']

# 所有endpoint的meta信息
EP_META = {}
EP_INFO_LIST = []
EP_INFOS = {}

# 权限组(必须存在于数据库, 项目启动后自动导入)
Group = namedtuple('group', ['name', 'info', 'id'])
AUTH_GROUPS = {
    # System 系统(金峰)
    # 'SYS_SUPER': Group('系统超级管理员', '', ''),
    'SYS_ADMIN': Group('系统管理员', '', ''),
    # Company 企业
    'CO_SUPER': Group('企业超级管理员', '', ''),
    'CO_ADMIN': Group('企业管理员', '', ''),
    'CO_PROJECT': Group('项目管理员', '', ''),
    'CO_OPERATE': Group('运维管理员', '', ''),
    'CO_USER': Group('普通员工', '', ''),
    # Agent 代理商
    'AGENT': Group('代理商', '', ''),
    # Guest 访客
    'GUEST': Group('访客', '', '')
}

# token
tmp_token = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4Mzk3NjE5NCwiZXhwIjoxNTg2NTY4MTk0fQ.eyJ1aWQiOiI1ZTY4NDQ4YTQ1YjY5YzdiNzc5MGIyYzYiLCJ0eXBlIjoxMDEsInNjb3BlIjoiU3lzU3VwZXJTY29wZSJ9.BM487QjEFINNKxrTgcd0YDoVvLuFJpVBjTlc3smzQ1wm1amSGYU1EaiLearM5SKtQEiugdWil03Wnj9H5Rkclw'

from app.libs.schedule_task import per_hour_statistics, per_day_statistics

JOBS = [
    {
        "id": "per_hour_statistics",
        "func": per_hour_statistics,
        "trigger": {
            "type": "cron",
            "hour": "*"
        },
        "replace_existing": True
    },
    {
        "id": "per_day_statistics",
        "func": per_day_statistics,
        "trigger": {
            "type": "cron",
            "day": "*"
        },
        "replace_existing": True
    }
]
