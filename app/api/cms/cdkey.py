# -*- coding: utf-8 -*-

from flask import request, g
from app.libs.redprint import RedPrint
from app.models.company import Company
from app.models.project import Project
from app.models.user import User as UserModel
from app.libs.token_auth import auth
from app.models.cdkey import CDKey
from bson.objectid import ObjectId
from app.libs.error_code import Success
from app.api_docs.cms import cdkey as api_doc
from app.validators.cdkey import CreateCDKeyValidator, CDKeyValidator, UpdateCDKeyValidator
from app.validators.params import PaginateValidator

api = RedPrint(name='cdkey', description='激活码管理', api_doc=api_doc, alias='cms_cdkey')



@api.route('', methods=['GET'])
@api.doc(args=['g.query.cdkey'], auth=True)
@auth.login_required
def get_cdkey():
    '''解析激活码内容'''
    cdkey_code = CDKeyValidator().validate_for_api().cdkey.data
    cdkey = CDKey.objects.filter(cdkey=cdkey_code).first_or_404()
    return Success(cdkey)


@api.route('', methods=['POST'])
@api.route_meta(auth='生成激活码', module='激活码')
@api.doc(args=['g.body.company_id', 'g.body.project_id', 'g.body.auth', 'g.body.group_id'], auth=True)
@auth.group_required
def create_cdkey():
    '''(企业管理员)生成激活码\n\t
        用于「企业管理员\项目负责人\运维员工\普通员工」的激活码
    '''
    user_id = g.user.uid
    validator = CreateCDKeyValidator().validate_for_api()
    company_id = validator.company_id.data
    project_id = validator.project_id.data
    group_id = validator.project_id.data # 权限组ID
    auth = validator.auth.data
    company = Company.objects.filter(id=company_id).first_or_404()
    company_name = company.name
    project = Project.objects.filter(id=project_id).first()
    project_name = ''
    if project:
        project_name = project.name
    # 生成CDKey
    hashkey = CDKey.generate_hashkey(company_name, company_id, auth, group_id, project_name, project_id)
    cdkey_code = CDKey.generate_cdkey()
    cdkey = CDKey.save_cdkey(user_id, hashkey, cdkey_code, auth, group_id, company_id, project_id)
    return Success(cdkey)


@api.route('', methods=['DELETE'])
@api.route_meta(auth='删除激活码', module='激活码')
@api.doc(args=['g.query.cdkey'], auth=True)
@auth.group_required
def delete_cdkey():
    '''删除激活码'''
    CDKeyValidator().validate_for_api().cdkey.data
    return Success(error_code=2)


@api.route('/state', methods=['PUT'])
@api.route_meta(auth='切换激活码状态', module='激活码')
@api.doc(args=['g.query.cdkey', 'query.state'], auth=True)
@auth.group_required
def edit_cdkey_state():
    '''改变激活码状态(激活or失效)'''
    validator = UpdateCDKeyValidator().validate_for_api()
    CDKey.toggle_state(cdkey=validator.cdkey.data, state=validator.state.data)
    return Success(error_code=1)



@api.route('/list', methods=['GET'])
@api.doc(args=['g.query.page', 'g.query.size'], auth=True)
@auth.login_required
def get_cdkey_list():
    '''获取(企业人员)激活码列表(找到自己生成
    '''
    validator = PaginateValidator().validate_for_api()
    page, size = validator.page.data, validator.size.data
    uid = g.user.uid
    cdkey_list = CDKey.objects.filter(gen_user=uid).paginate_to_package(page=page, per_page=size)
    return Success(cdkey_list)
