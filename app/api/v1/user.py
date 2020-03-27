# -*- coding: utf-8 -*-
"""
  ↓↓↓ 用户接口 ↓↓↓
"""
from flask import g

from app.libs.redprint import RedPrint
from app.libs.error_code import Success
from app.api_docs.v1 import user as api_doc
from app.libs.token_auth import auth
from app.models.user import User
from app.validators.forms import ResetPasswordValidator
from app.validators.user import UpdateUserValidator

api = RedPrint(name='user', description='用户', api_doc=api_doc)


@api.route('', methods=['GET'])
@api.doc(auth=True)
@auth.login_required
def get_user():
    '''用户获取自身信息'''
    user = User.get_current_user()
    return Success(user)


@api.route('', methods=['PUT'])
@api.doc(args=['realname', 'username', 'password', 'mobile', 'email'], auth=True)
@auth.login_required
def edit_user():
    '''用户编辑自身信息(小程序注册后)不能修改自己权限'''
    validator = UpdateUserValidator().validate_for_api()
    uid = g.user.uid

    user = User.objects.filter(id=uid).first_or_404(msg='用户不存在')
    user.username = validator.username.data
    user.realname = validator.realname.data
    user.mobile = validator.mobile.data
    user.email = validator.email.data
    user.password = validator.password.data
    user.save()

    return Success(user)


@api.route('/password', methods=['PUT'])
@api.doc(args=['g.body.new_password', 'g.body.confirm_password'], auth=True)
@auth.login_required
def change_password():
    '''更改密码'''
    password = ResetPasswordValidator().validate_for_api().new_password.data
    user = User.objects.filter(id=g.user.uid).first_or_404()
    user = user.update(password=password)
    return Success(user, error_code=1)


@api.route('/apply', methods=['POST'])
@api.doc()
def apply_permission():
    pass
