# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/5/31.
"""

from enum import Enum


class ClientTypeEnum(Enum):
    '''客户端登录方式类型'''
    USERNAME = 100  # 用户名
    EMAIL = 101  # 邮箱登录
    MOBILE = 102  # 手机登录
    # 微信
    WX_MINA = 200  # 微信小程序
    WX_OPEN = 201  # 微信第三方登录(Web端)
    WX_ACCOUNT = 202  # 微信第三方登录(公众号H5端)


# 是否为超级管理员的枚举
class AdminScopeEnum(Enum):
    USER = 1  # 普通用户
    ADMIN = 2  # 管理员


class ScopeEnum(Enum):
    '''
    1～9  : 系统管理员
    10～19: 企业管理员
    20~29 : 中间商
    999   : 游客
    用法：ScopeEnum.SYS_SUPER == ScopeEnum(1) # True
    '''
    USER = 1  # 普通用户
    ADMIN = 2  # 管理员

    # # System 系统(金峰)
    # SYS_SUPER = 1  # 系统超级管理员
    # SYS_ADMIN = 2  # 系统管理员
    # # Company 企业
    # CO_SUPER = 10  # 企业超级管理员
    # CO_ADMIN = 11  # 企业管理员
    # CO_PROJECT = 12  # 项目管理员
    # CO_OPERATE = 13  # 运维管理员
    # CO_USER = 14  # 普通员工
    # # Agent 代理商
    AGENT = 20  # 代理商
    # # guest 游客
    # GUEST = 999  # 游客


class DeviceLine(Enum):
    """
    00: 线路检测有电，旁路不受控制
    01: 正常
    10: 断电
    11: 跳闸
    """
    TRIP = "11"
    OFF = "10"
    NORMAL = "01"
    ABNORMAL = "00"


class ExcelTypeEnum(Enum):
    EMPTY = 0
    STRING = 1
    NUMBER = 2
    DATE = 3
    BOOLEAN = 4
    ERROR = 5
