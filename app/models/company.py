# -*- coding: utf-8 -*-
from flask import g, current_app
from app.libs.error_code import DuplicateException
from .base import Base
from mongoengine import StringField, ObjectIdField
from .cdkey import CDKey
from app.libs.scope import ScopeEnum


class Company(Base):
    """
    公司表
    """
    name = StringField()  # 公司名
    manager_name = StringField()  # 公司负责人
    manager_id = ObjectIdField() # 公司负责人ID
    cdkey = StringField()  # 企业的CDKey
    meta = {
        'collection': 'company',
        'strict': True
    }

    @staticmethod
    def create(company_name):
        '''新建企业，并生成对应的
        权限: 系统超级管理员、系统管理员、中间商
        :param company_name:
        :return:
        '''
        user_id = g.user.uid
        group_id = current_app.config['AUTH_GROUPS']['CO_SUPER'].id  # 企业超级管理员的Group ID
        company = Company(name=company_name) # 先生成id给CDKey
        hashkey = CDKey().generate_hashkey(company_name=company_name,
                                           company_id=company.id,
                                           auth=1,
                                           group_id=group_id)
        cdkey = CDKey().generate_cdkey()
        CDKey.save_cdkey(user_id, hashkey, cdkey, auth=1, group_id=group_id, company_id=company.id)
        company.cdkey = cdkey
        company.save()
        return company

