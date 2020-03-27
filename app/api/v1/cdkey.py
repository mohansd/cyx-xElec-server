# -*- coding: utf-8 -*-
from app.libs.enums import ScopeEnum
from app.libs.error import APIException
from app.libs.redprint import RedPrint
from app.models.user import User
from app.libs.token_auth import auth
from app.models.cdkey import CDKey as CDKeyModel
from bson.objectid import ObjectId
from flask import g
from app.libs.error_code import Success
from app.api_docs.v1 import cdkey as api_doc
from app.service.user_active import UserActive
from app.validators.base import BaseValidator

api = RedPrint(name='cdkey', description='激活码', api_doc=api_doc)

@api.route('/active', methods=['PUT'])
@api.doc(args=['cdkey',
               '*str.body.username', '*str.body.realname',
               '*str.body.password', '*str.body.mobile',
               '*str.body.email'], body_desc='cdkey', auth=True)
@auth.login_required
def active_cdkey():
    '''激活激活码(企业级以下的用户的注册)'''
    validator = BaseValidator().get_json()
    uid = g.user.uid
    cdkey_code = validator['cdkey']
    username = validator['username']
    realname = validator['realname']
    password = validator['password']
    mobile = validator['mobile']
    email = validator['email']

    cdkey = CDKeyModel.objects.filter(cdkey=cdkey_code, state=True).first_or_404(msg='激活码无效，请联系相关负责人')
    employee_tuple = (ScopeEnum.CO_PROJECT,
                      ScopeEnum.CO_OPERATE,
                      ScopeEnum.CO_USER
                      )
    if ScopeEnum(cdkey.auth) == ScopeEnum.CO_SUPER:
        # 注册成企业超级管理员
        UserActive.active_co_super_or_admin(cdkey, uid, username, realname, password, mobile, email)
        cdkey.state = False
        cdkey.save()
    elif ScopeEnum(cdkey.auth) == ScopeEnum.CO_ADMIN:
        UserActive.active_co_super_or_admin(cdkey, uid, username, realname, password, mobile, email)
    elif  ScopeEnum(cdkey.auth) in employee_tuple:
        UserActive.active_co_employee(cdkey, uid, username, realname, password, mobile, email)
    else:
        raise APIException(msg='激活码权限不足')
    return Success()
