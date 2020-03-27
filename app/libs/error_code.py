# -*- coding: utf-8 -*-

from app.libs.error import APIException
from flask import json
from app.libs.utils import jsonify


class Success(APIException):
    code = 200
    error_code = 0
    data = None
    msg = '成功'

    def __init__(self, data=None, code=None, error_code=None, msg=None):
        if data:
            self.data = jsonify(data)
        if error_code == 1:
            code = code if code else 201
            msg = msg if msg else '创建 | 更新成功'
        if error_code == 2:
            code = code if code else 202
            msg = msg if msg else '删除成功'
        super(Success, self).__init__(code, error_code, msg)

    def get_body(self, environ=None):
        body = dict(
            error_code=self.error_code,
            msg=self.msg,
            data=self.data
        )
        text = json.dumps(body)
        return text


class ForbiddenException(APIException):
    code = 200
    error_code = 1004
    msg = 'forbidden, not in scope'


class NotFound(APIException):
    code = 200
    error_code = 1001
    msg = '未查询到数据'


class ServerError(APIException):
    code = 500
    error_core = 999
    msg = '服务器异常'


class DuplicateException(APIException):
    code = 200
    error_code = 2001
    msg = '数据已存在'


class ClientTypeError(APIException):
    code = 200
    error_code = 1006
    msg = 'clinet is invalid'


class ParameterException(APIException):
    code = 200
    error_code = 1000
    msg = 'invalid parameter'


class TokenException(APIException):
    code = 200
    error_code = 1001
    msg = 'Token已过期或无效Token'


class AuthFailed(APIException):
    code = 200
    error_code = 1005
    msg = 'authorization failed'


class RepeatException(APIException):
    code = 200
    error_code = 2001
    msg = '重复数据'


class UserException(NotFound):
    code = 200
    error_code = 6000
    msg = '用户不存在'


class ExcelHeadException(NotFound):
    code = 200
    error_code = 7001
    msg = 'Excel表格表头信息缺少'


class WeChatException(ServerError):
    code = 500
    error_code = 999
    msg = '微信服务器接口调用失败'


class DeviceException(NotFound):
    code = 200
    error_code = 998
    msg = '设备未在线'
