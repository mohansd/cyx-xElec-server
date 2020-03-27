# _*_ coding: utf-8 _*_

from app.libs.redprint import RedPrint
from app.libs.error_code import Success
from app.api_docs.cms import project as api_doc
from app.libs.token_auth import auth
from app.models.project import Project
from app.validators.base import BaseValidator
from app.validators.params import PaginateValidator

api = RedPrint(name='project', description='项目管理', api_doc=api_doc, alias='cms_project')


@api.route('/list', methods=['GET'])
@api.route_meta(auth='查询项目列表', module='项目')
@api.doc(args=['g.query.page', 'g.query.size'], auth=True)
@auth.group_required
def get_list():
    '''查询项目列表(分页)'''
    validator = PaginateValidator().validate_for_api()
    page, size = validator.page.data, validator.size.data
    return Success()


@api.route('/<string:project_id>', methods=['GET'])
@api.route_meta(auth='查询项目详情', module='项目')
@api.doc(args=['g.path.project_id'], auth=True)
@auth.group_required
def get_one(project_id):
    '''查询项目详情'''
    project = Project.get_or_404(id=project_id)
    return Success(project)


@api.route('', methods=['POST'])
@api.route_meta(auth='新建项目', module='项目')
@api.doc(auth=True)
@auth.group_required
def create_one():
    '''新建项目'''
    form = BaseValidator().get_json()
    project = Project.create(**form)
    return Success(error_code=1)


@api.route('/<string:project_id>', methods=['POST'])
@api.route_meta(auth='编辑项目', module='项目')
@api.doc(args=['g.path.project_id'], auth=True)
@auth.group_required
def edit_one(project_id):
    '''编辑项目'''
    form = BaseValidator().get_json() 
    project = Project.get_or_404(id=project_id)
    project.renew(**form)
    return Success(error_code=1)


@api.route('/<string:project_id>', methods=['DELETE'])
@api.route_meta(auth='删除项目', module='项目')
@api.doc(args=['g.path.project_id'], auth=True)
@auth.group_required
def delete_one(project_id):
    '''删除项目'''
    project = Project.get_or_404(id=project_id)
    project.delete()
    return Success(error_code=2)
