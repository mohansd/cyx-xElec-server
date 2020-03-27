# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/3/24.
  ↓↓↓ 权限管理接口 ↓↓↓
"""
from app.libs.core import get_ep_name, find_auth_module
from app.libs.error_code import Success
from app.libs.redprint import RedPrint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.auth import Auth as AuthModel
from app.api_docs.cms import auth as api_doc
from app.validators.forms import AuthsValidator

__author__ = 'Allen7D'

api = RedPrint(name='auth', description='权限管理', api_doc=api_doc, alias='cms_auth')


@api.route('/append', methods=['POST'])
@api.route_meta(auth='新增多个权限', module='管理员', mount=False)
@api.doc(args=['g.body.group_id', 'g.body.auth_ids'], auth=True)
@auth.admin_required
def update_auth_list():
    '''添加多个权限(到某个权限组)'''
    validator = AuthsValidator().validate_for_api()
    auth_list = [get_ep_name(id) for id in validator.auth_ids.data]
    group_id = validator.group_id.data

    for auth in auth_list:
        one = AuthModel.get(group_id=group_id, auth=auth)
        if not one:
            meta = find_auth_module(auth)
            AuthModel.create(group_id=group_id, auth=meta.auth, module=meta.module)
    return Success(error_code=1)


@api.route('/remove', methods=['POST'])
@api.route_meta(auth='删除多个权限', module='管理员', mount=False)
@api.doc(args=['g.body.group_id', 'g.body.auth_ids'], auth=True)
@auth.admin_required
def delete_auth_list():
    '''删除多个权限(从某个权限组)'''
    validator = AuthsValidator().validate_for_api()
    auth_list = [get_ep_name(id) for id in validator.auth_ids.data]
    group_id = validator.group_id.data


    db.session.query(AuthModel).filter(
        AuthModel.auth.in_(auth_list),
        AuthModel.group_id == group_id
    ).delete(synchronize_session=False)
    return Success(error_code=2)
