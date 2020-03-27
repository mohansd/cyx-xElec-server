# _*_ coding: utf-8 _*_
"""
	基础的CRUD都是放在CMS中
	频繁的业务操作放在V1
"""
from flask import g, current_app

from app.libs.redprint import RedPrint
from app.libs.error_code import Success
from app.api_docs.cms import user as api_doc
from app.libs.token_auth import auth
from app.models.user import User as UserModel
from app.libs.scope import ScopeEnum
from app.validators.base import BaseValidator
from app.validators.forms import ResetPasswordValidator, UpdateAdminValidator
from app.validators.params import PaginateValidator
from app.validators.user import CreateUserValidator, FilterUserValidator, UserValidator, UpdateUserValidator

api = RedPrint(name='user', description='用户管理', api_doc=api_doc, alias='cms_user')


@api.route('/list', methods=['GET'])
@api.route_meta(auth='查询用户列表', module='用户')
@api.doc(args=['g.query.page', 'g.query.size', 'g.query.company_id', 'g.query.group_id'], auth=True)
@auth.group_required
def get_user_list():
    '''获取员工列表(分页)\n\t
    该接口主要是获取非代理商

    还需要知道用户的auth获取比他权利小的用户
       授权/收权的bug，如果2个权利给予呢
       权利涉及到:auth 和 project
           ==> user包含project_id_list
           ==> 如果快速查询到该user下的project_list呢？(难点)
    '''
    agent_group_id = current_app.config['AUTH_GROUPS']['AGENT'].id
    paginate = PaginateValidator().validate_for_api().data
    page, size = paginate['page'], paginate['size']
    query_condition = FilterUserValidator().validate_for_api().data
    user_list_package = UserModel.objects(group_id__ne=agent_group_id)\
        .filter(**query_condition) \
        .paginate_to_package(page=page, per_page=size)
    return Success(user_list_package)


@api.route('/<string:uid>', methods=['GET'])
@api.route_meta(auth='查询用户详情', module='用户')
@api.doc(args=['uid'], auth=True)
@auth.group_required
def get_user(uid):
    '''获取用户信息(管理员)'''
    uid = UserValidator().validate_for_api().uid.data
    user = UserModel.get_or_404(id=uid, msg='该用户不存在')
    return Success(user)


@api.route('', methods=['POST'])
@api.route_meta(auth='新建用户', module='用户')
@api.doc(args=['g.body.realname', 'g.body.username',
               'g.body.password', 'g.body.mobile',
               'g.body.email', 'g.body.auth',
               'g.body.company_id'], auth=True)
@auth.group_required
def create_user():
    '''新建用户(管理者或员工)\n\t
    权限不够则不能使用
    默认密码123456
    '''
    form = CreateUserValidator().validate_for_api().data
    user = UserModel.create(**form)
    return Success(user)


@api.route('/<string:uid>', methods=['PUT'])
@api.route_meta(auth='编辑用户', module='用户')
@api.doc(args=['g.path.uid', 'g.body.auth',
               'g.body.realname', 'g.body.username',
               'g.body.mobile', 'g.body.email', 'g.body.auth',
               'g.body.company_id'], auth=True)
@auth.group_required
def edit_user(uid):
    '''更新用户信息(管理员)'''
    uid = UserValidator().validate_for_api().uid.data
    form = UpdateUserValidator().validate_for_api().data
    user = UserModel.objects.filter(id=uid).first_or_404()
    user = user.renew(**form)
    return Success(user, error_code=1)


@api.route('/<string:uid>/group', methods=['PUT'])
@api.route_meta(auth='切换用户分组', module='用户')
@api.doc(args=['g.path.uid+', 'g.body.group_id'], auth=True)
@auth.group_required
def change_user_group(uid):
    '''更新用户信息(仅能重新分组)'''
    group_id = UpdateAdminValidator().validate_for_api().group_id.data
    user = UserModel.get_or_404(id=uid)
    user.update(group_id=group_id)
    return Success(error_code=1)


@api.route('/<string:uid>', methods=['DELETE'])
@api.route_meta(auth='删除用户', module='用户')
@api.doc(args=['uid'], auth=True)
@auth.group_required
def delete_user(uid):
    '''删除用户(管理员)'''
    validator = BaseValidator().get_json()  # 快速获取所有的非校验的参数
    return Success(validator, error_code=2)


@api.route('/<string:uid>/password', methods=['PUT'])
@api.route_meta(auth='更改用户密码', module='用户')
@api.doc(args=['uid', 'g.body.new_password', 'g.body.confirm_password'], auth=True)
@auth.group_required
def change_user_password(uid):
    '''修改用户的密码'''
    password = ResetPasswordValidator().validate_for_api().new_password.data
    user = UserModel.objects.filter(id=uid).first_or_404()
    user = user.renew(password=password)
    return Success(user, error_code=1)
