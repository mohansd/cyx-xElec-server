# _*_ coding: utf-8 _*_
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
	SignatureExpired, BadSignature

from app.libs.error_code import AuthFailed

class Token():
	@staticmethod
	def decrypt(token):
		'''解析token的信息
		:param token:
		:return: 该token的权限、用户ID、创建时间、有效期
		'''
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token, return_header=True) # token在POST中
		except BadSignature:
			raise AuthFailed(msg='token失效，请重新登录', error_code=1002)
		except SignatureExpired:
			raise AuthFailed(msg='token过期，请重新登录', error_code=1003)

		r = {
			'scope': data[0]['scope'], # 用户权限
			'uid': data[0]['uid'], # 用户ID
			'create_at': data[1]['iat'],  # 创建时间
			'expire_in': data[1]['exp']  # 有效期
		}

		return r
