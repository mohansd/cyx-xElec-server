# _*_ coding: utf-8 _*_
from app.libs.swagger_filed import (IntegerQueryFiled, StringQueryFiled, IntegerPathFiled,
                                    StringPathFiled, BodyField, inject)


uid = StringPathFiled(name='uid',
                      description="用户ID",
                      enum=['5e68447445b69c7b7790b2c5',
                            '5e68448a45b69c7b7790b2c6',
                            '0017be56959511e8b3470016',
                            '001aa40c61c111e8a8a60016',
                            '001ea0984fa111e8a3d40016'],
                      default='5e68447445b69c7b7790b2c5',
                      required=True)

realname = BodyField('realname', 'string', '用户真名', ['董冬伟'])
username = BodyField('username', 'string', '用户名', ['Allen7D'])
password = BodyField('password', 'string', '密码(不输则默认: 123456)', ['123456'])
mobile = BodyField('mobile', 'string', '手机号', ['13758787058'])
email = BodyField('email', 'string', '邮箱', ['462870781@qq.com'])
auth = BodyField('auth', 'integer', '权限(数字: 1,2,10,11,12,13,14,19)', [1, 2, 10, 11, 12, 13, 14, 19])
company_id = BodyField('company_id', 'string', '公司id', ['5e6784a3d01446cf375d6d37'])

