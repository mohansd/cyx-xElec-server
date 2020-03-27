# _*_ coding: utf-8 _*_
"""
  ↓↓↓ Token接口 ↓↓↓
"""
from flask import current_app

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success
from app.libs.redprint import RedPrint
from app.models.user import User
from app.service.token_service import Token
from app.libs.token_auth import generate_auth_token
from app.validators.forms import ClientValidator, TokenValidator
from app.api_docs.v1 import token as api_doc

__author__ = 'Allen7D'

api = RedPrint(name='token', description='登录令牌', api_doc=api_doc)


@api.route('', methods=['POST'])
@api.doc(args=['account', 'secret', 'type'], body_desc='''登录的基本信息: 账号、密码、登录类型:
                                                            - 账号账号登录(type:100)
                                                            - 手机账号登录(type:102)
                                                            - 小程序登录(type:200)
                                                            - 微信扫码登录(type:201)''')
def get_token():
    '''生成「令牌」(4种登录方式)'''
    form = ClientValidator().validate_for_api()
    promise = {
        ClientTypeEnum.USERNAME: User.verify_by_username,  # 用户名&密码登录
        ClientTypeEnum.EMAIL: User.verify_by_email,  # 邮箱&密码登录
        ClientTypeEnum.MOBILE: User.verify_by_mobile,  # 手机号&密码登录
        ClientTypeEnum.WX_MINA: User.verify_by_wx_mina,  # 微信·小程序登录
    }
    # 微信登录, 则account为code(需要微信小程序调用wx.login接口获取), secret为空
    identity = promise[ClientTypeEnum(form.type.data)](form.account.data, form.secret.data)
    # token生成
    expiration = current_app.config['TOKEN_EXPIRATION']  # token有效期
    token = generate_auth_token(identity['uid'],
                                form.type.data.value,
                                identity['scope'],
                                expiration)
    return Success(data=token)


@api.route('/verify', methods=['POST'])
@api.doc(args=['token'], body_desc='令牌')
def decrypt_token():
    """解析「令牌」"""
    token = TokenValidator().validate_for_api().token.data
    result = Token.decrypt(token)
    return Success(data=result)
