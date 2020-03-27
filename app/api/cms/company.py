# -*- coding: utf-8 -*-
from app.libs.error_code import Success, ForbiddenException
from app.libs.redprint import RedPrint

from app.libs.token_auth import auth
from app.models.company import Company
from app.models.user import User as UserModel
from bson.objectid import ObjectId
from app.api_docs.cms import company as api_doc
from app.validators.company import CreateCompanyValidator, EditCompanyValidator
from app.validators.params import PaginateValidator

api = RedPrint(name='company', description='公司管理', api_doc=api_doc, alias='cms_company')


@api.route('/<string:id>', methods=['GET'])
@api.route_meta(auth='查询公司详情', module='公司')
@api.doc(args=['g.path.company_id'], auth=True)
@auth.group_required
def get_company(id):
    '''查询公司详情'''
    company = Company.objects.filter(id=id).first_or_404()
    return Success(company)


@api.route('/list', methods=['GET'])
@api.route_meta(auth='查询公司列表', module='公司')
@api.doc(args=['g.query.page', 'g.query.size'], auth=True)
@auth.group_required
def get_company_list():
    '''查询公司列表'''
    validator = PaginateValidator().validate_for_api()
    page, size = validator.page.data, validator.size.data
    company_list_package = Company.objects.paginate_to_package(page=page, per_page=size)
    return Success(company_list_package)


@api.route('', methods=['POST'])
@api.route_meta(auth='新建公司', module='公司')
@api.doc(args=['g.body.company_name'], auth=True)
@auth.group_required
def create_company():
    '''新建公司'''
    company_name = CreateCompanyValidator().validate_for_api().company_name.data
    res = Company.create(company_name=company_name)
    return Success()


@api.route('/<string:id>', methods=['PUT'])
@api.route_meta(auth='编辑公司', module='公司')
@api.doc(args=['g.body.company_id', 'g.body.company_name'], auth=True)
@auth.login_required
def edit_company(id):
    '''编辑公司'''
    validator = EditCompanyValidator().validate_for_api()
    company = Company.objects.filter(id=id).first_or_404()
    company["name"] = validator.company_name.data
    company.save()
    return Success(company, error_code=1)


@api.route('/<string:id>', methods=['DELETE'])
@api.route_meta(auth='删除公司', module='公司')
@api.doc(args=['g.body.company_id'], auth=True)
@auth.login_required
def delete_company(id):
    '''删除公司'''
    company = Company.objects.filter(id=id).first_or_404()
    if UserModel.get(company_id=company.id):
        raise ForbiddenException(msg='该公司下存在员工，不可删除')
    company.delete()
    return Success(error_code=2)
