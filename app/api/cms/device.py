# _*_ coding: utf-8 _*_


from app.libs.redprint import RedPrint
from app.libs.error_code import Success
from app.api_docs.cms import device as api_doc
from app.libs.token_auth import auth
from app.models.device import Device
from app.service.excel_file import ExcelService
from app.validators.params import PaginateValidator
from app.validators.project import UploadExcelValidator

api = RedPrint(name='device', description='设备管理', api_doc=api_doc, alias='cms_device')


@api.route('/list', methods=['GET'])
@api.route_meta(auth='查询设备列表', module='设备')
@api.doc(args=['g.query.page', 'g.query.size'], auth=True)
@auth.group_required
def get_list():
    '''获取设备列表(分页)'''
    validator = PaginateValidator().validate_for_api()
    page, size = validator.page.data, validator.size.data
    device_list_package = Device.objects.filter().paginate_to_package(page=page, per_page=size)
    return Success(device_list_package)


@api.route('/<string:device_id>', methods=['DELETE'])
@api.route_meta(auth='删除设备', module='设备')
@api.doc(auth=True)
@auth.group_required
def delete_one(device_id):
    '''删除设备'''
    return Success(error_code=2)


@api.route('/upload', methods=['POST'])
@api.route_meta(auth='上传设备Excel表', module='设备')
@api.doc(auth=True)
@auth.group_required
def upload_file():
    '''上传设备录入信息(excle文件)'''
    file = UploadExcelValidator().validate_for_api().file.data
    res = ExcelService(file).load_data()
    return Success(data=res, error_code=1)

# @api.route('/download/<string: file_name>', methods=['GET'])
# @api.doc(args=['path.file_name'], auth=True)
# @auth.login_required
# def download_file(file_name):
#     '''下载设备信息excle'''
#     return Success()
