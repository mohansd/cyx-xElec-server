# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/3/24.
  ↓↓↓ 管理员管理接口 ↓↓↓
"""
from flask import current_app, request

from app.libs.error_code import Success
from app.libs.redprint import RedPrint
from app.libs.token_auth import auth
from app.models.base import db
from app.libs.enums import ScopeEnum
from app.models.user import User as UserModel
from app.api_docs.cms import admin as api_doc
from app.validators.forms import PaginateValidator, ResetPasswordValidator, CreateAdminValidator

__author__ = 'Allen7D'

api = RedPrint(name='admin', description='管理员管理', api_doc=api_doc, alias='cms_admin')


@api.route('/auths', methods=['GET'])
@api.route_meta(auth='查询所有可分配的权限', module='管理员', mount=False)
@api.doc(auth=True)
@auth.admin_required
def get_auths():
    '''查询所有可分配的权限'''
    endpoint_info_list = current_app.config['EP_INFOS']
    return Success(endpoint_info_list)


@api.route('/list', methods=['GET'])
@api.route_meta(auth='查询各级用户列表', module='管理员', mount=False)
@api.doc(args=['g.query.page', 'g.query.size', 'query.group_id'], auth=True)
@auth.admin_required
def get_admin_list():
    '''获取各级用户列表'''
    validator = PaginateValidator().validate_for_api()
    page, size = validator.page.data, validator.size.data
    group_id = request.args.get('group_id')
    query_condition = {
        'auth': ScopeEnum.ADMIN.value,  # 至少是管理员
        'group_id': group_id
    } if group_id else {
        'auth': ScopeEnum.ADMIN.value
    }
    user_list = UserModel.get_all(**query_condition)
    return Success(user_list)


@api.route('', methods=['POST'])
@api.route_meta(auth='新增管理员', module='管理员', mount=False)
@api.doc(args=['g.body.username', 'g.body.password', 'g.body.confirm_password',
               'g.body.group_id', 'g.body.email', 'g.body.mobile'], auth=True)
@auth.admin_required
def create_admin():
    '''新增管理员'''
    form = CreateAdminValidator().validate_for_api()
    UserModel.is_exist_to_404(username=form.username.data, msg='用户名重复，请重新输入')
    UserModel.create(auth=ScopeEnum.ADMIN.value, **form.data)
    return Success()


@api.route('/<string:uid>', methods=['PUT'])
@api.route_meta(auth='更新管理员', module='管理员', mount=False)
@api.doc(auth=True)
@auth.admin_required
def update_admin(uid):
    '''更新管理员'''
    user = UserModel.get_or_404(id=uid, msg='用户不存在')
    return Success(user)


@api.route('/<string:uid>', methods=['GET'])
@api.route_meta(auth='删除管理员', module='管理员', mount=False)
@api.doc(auth=True)
@auth.admin_required
def delete_admin(uid):
    '''删除管理员'''
    user = UserModel.get_or_404(id=uid, msg='用户不存在')
    user.delete()
    return Success()


@api.route('/password/<string:uid>', methods=['PUT'])
@api.route_meta(auth='修改管理员密码', module='管理员', mount=False)
@api.doc(auth=True)
@auth.admin_required
def change_user_password(uid):
    form = ResetPasswordValidator().validate_for_api()
    user = UserModel.get_or_404(id=uid, msg='用户不存在')
    user.update(password=form.new_password.data)
    return Success(msg='密码修改成功')


@api.route('/active/<string:uid>', methods=['PUT'])
@api.doc(args=['g.path.uid'], auth=True)
@auth.admin_required
def trans2active(uid):
    '''激活管理员'''
    return Success(msg='操作成功')


@api.route('/disable/<string:uid>', methods=['PUT'])
@api.doc(args=['g.path.uid'], auth=True)
@auth.admin_required
def trans2disable(uid):
    '''禁用管理员'''
    return Success(msg='操作成功')
