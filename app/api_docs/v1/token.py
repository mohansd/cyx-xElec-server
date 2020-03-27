# _*_ coding: utf-8 _*_

from app.libs.swagger_filed import BodyField, inject
from app.config.setting import tmp_token

token = BodyField('token', 'string', 'Token', [tmp_token])
account = BodyField('account', 'string', '邮箱', ["462870781@qq.com"])
secret = BodyField('secret', 'string', '密码', ["123456"])
type = BodyField('type', 'integer', '登录方式', [101])