# _*_ coding: utf-8 _*_
"""
  ↓↓↓ 代理商管理接口 ↓↓↓
"""
from flask import current_app

from app.libs.redprint import RedPrint
from app.libs.error_code import Success
from app.api_docs.cms import agent as api_doc
from app.libs.token_auth import auth
from app.models.user import User
from app.libs.scope import ScopeEnum
from app.validators.agent import CreateAgentValidator, UpdateAgentValidator
from app.validators.params import PaginateValidator

api = RedPrint(name='agent', description='代理商管理', api_doc=api_doc, alias='cms_agent')


@api.route('/list', methods=['GET'])
@api.route_meta(auth='查询代理商列表', module='代理商')
@api.doc(args=['g.query.page', 'g.query.size'], auth=True)
@auth.group_required
def get_list():
    '''获取代理商列表(分页)
    '''
    group_id = current_app.config['AUTH_GROUPS']['AGENT'].id  # 代理商的Group ID
    validator = PaginateValidator().validate_for_api()
    page, size = validator.page.data, validator.size.data
    user_list_package = User.objects.filter(group_id=group_id).paginate_to_package(page=page, per_page=size)
    return Success(user_list_package)


@api.route('/<string:uid>', methods=['GET'])
@api.route_meta(auth='查询代理商详情', module='代理商')
@api.doc(args=['path.uid+'], auth=True)
@auth.group_required
def get_one(uid):
    '''获取代理商信息'''
    group_id = current_app.config['AUTH_GROUPS']['AGENT'].id  # 代理商的Group ID
    user = User.objects.filter(id=uid, group_id=group_id)\
        .first_or_404()
    return Success(user)


@api.route('/<string:uid>', methods=['PUT'])
@api.route_meta(auth='编辑代理商', module='代理商')
@api.doc(args=['path.uid+', 'g.body.realname',
               'g.body.username', 'g.body.mobile', 'g.body.company_name'], auth=True)
@auth.group_required
def edit_one(uid):
    '''更新代理商信息'''
    group_id = current_app.config['AUTH_GROUPS']['AGENT'].id  # 代理商的Group ID
    form = UpdateAgentValidator().validate_for_api().data
    user = User.get_or_404(id=uid, group_id=group_id)
    user = user.renew(**form)
    return Success(user, error_code=1)


@api.route('/<string:uid>', methods=['DELETE'])
@api.route_meta(auth='删除代理商', module='代理商')
@api.doc(args=['path.uid+'], auth=True)
@auth.group_required
def delete_one(uid):
    '''删除代理商(谨用)'''
    group_id = current_app.config['AUTH_GROUPS']['AGENT'].id  # 代理商的Group ID
    user = User.objects.filter(id=uid, group_id=group_id).first_or_404()
    return Success(user, error_code=2)


@api.route('', methods=['POST'])
@api.doc(args=['g.body.realname', 'g.body.username',
               'g.body.password', 'g.body.mobile', 'g.body.company_name'], auth=True)
@auth.group_required
def create_one():
    '''新建代理商(管理者或员工)\n\t
       公司名字，就是代理商的公司
    '''
    group_id = current_app.config['AUTH_GROUPS']['AGENT'].id  # 代理商的Group ID
    validator = CreateAgentValidator().validate_for_api()
    user = User(
        username=validator.username.data,
        realname=validator.realname.data,
        mobile=validator.mobile.data,
        email=validator.email.data,
        auth=ScopeEnum.AGENT.value,
        group_id=group_id,
        company_name=validator.company_name.data
    )
    user.password = validator.password.data
    user.save()
    return Success(user)
