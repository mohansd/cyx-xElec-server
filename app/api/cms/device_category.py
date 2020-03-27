# _*_ coding: utf-8 _*_
"""
    设备类型(按照规格化分)
"""
from app.libs.redprint import RedPrint
from app.libs.error_code import Success, ForbiddenException
from app.api_docs.cms import device_category as api_doc
from app.libs.token_auth import auth
from app.models.device import Device as DeviceModel
from app.models.device_category import DeviceCategory
from app.validators.base import BaseValidator
from app.validators.params import PaginateValidator

api = RedPrint(name='device_category', description='设备类别(规格)管理', api_doc=api_doc, alias='cms_device_category')


@api.route('/list', methods=['GET'])
@api.route_meta(auth='查询设备类型列表', module='设备类型')
@api.doc(args=['g.query.page', 'g.query.size'], auth=True)
@auth.group_required
def get_list():
    '''查询设备类型列表(分页)'''
    validator = PaginateValidator().validate_for_api()
    page, size = validator.page.data, validator.size.data
    category_list_package = DeviceCategory.objects.filter().paginate_to_package(page=page, per_page=size)
    return Success(category_list_package)


@api.route('/<string:category_id>', methods=['GET'])
@api.route_meta(auth='查询设备类型详情', module='设备类型')
@api.doc(args=['path.category_id'], auth=True)
@auth.group_required
def get_one(category_id):
    '''查询设备类型详情'''
    device_category = DeviceCategory.get_or_404(id=category_id)
    return Success(device_category)


@api.route('', methods=['POST'])
@api.route_meta(auth='新建设备类型', module='设备类型')
@api.doc(args=['*str.body.name',
               '*str.body.specs', '*int.body.total_capacity',
               '*int.body.elec_limit', '*int.body.warranty_year'], auth=True)
@auth.group_required
def create_one():
    '''新建设备类型详情'''
    form = BaseValidator().get_json()
    device_category = DeviceCategory.create(**form)
    return Success(data=device_category, error_code=1)


@api.route('/<string:category_id>', methods=['PUT'])
@api.route_meta(auth='更新设备类型', module='设备类型')
@api.doc(args=['path.category_id', '*str.body.name',
               '*str.body.specs', '*int.body.total_capacity',
               '*int.body.elec_limit', '*int.body.warranty_year'], auth=True)
@auth.group_required
def edit_one(category_id):
    '''更新设备类型详情'''
    validator = BaseValidator().get_json()
    category_id = validator.pop('category_id', None)
    device_category = DeviceCategory.get_or_404(id=category_id)
    device_category.renew(**validator)
    return Success(data=device_category, error_code=1)


@api.route('/<string:category_id>', methods=['DELETE'])
@api.route_meta(auth='删除设备类型', module='设备类型')
@api.doc(args=['path.category_id'], auth=True)
@auth.group_required
def delete_one(category_id):
    '''删除设备类型/n/t
    如果设备已经绑定了该类型，无法删除'''
    device_category = DeviceCategory.get_or_404(id=category_id)
    if DeviceModel.get(category_id=category_id):
        raise ForbiddenException(msg='该类别下存在设备，不可删除')
    device_category.delete()
    return Success(error_code=2)
