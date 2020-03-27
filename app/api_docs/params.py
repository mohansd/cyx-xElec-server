# _*_ coding: utf-8 _*_
from app.libs.swagger_filed import StringPathFiled, IntegerQueryFiled, StringQueryFiled, BodyField

id = StringPathFiled(name='id',
                     description="ObjectId",
                     enum=['5e6784a3d01446cf375d6d37',
                           '5e6784afd01446cf375d6d38',
                           '0017be56959511e8b3470016',
                           '001aa40c61c111e8a8a60016',
                           '001ea0984fa111e8a3d40016'],
                     default='5e6784a3d01446cf375d6d37',
                     required=True).data

company_id = StringQueryFiled(name='company_id',
                              description="公司ID",
                              enum=['5e6784a3d01446cf375d6d37',
                                    '5e6784afd01446cf375d6d38',
                                    '0017be56959511e8b3470016',
                                    '001aa40c61c111e8a8a60016',
                                    '001ea0984fa111e8a3d40016'],
                              default='5e6784a3d01446cf375d6d37',
                              required=True).data
company_id_in_query = company_id

user_id = StringPathFiled(name='uid',
                          description="用户ID",
                          enum=['5e68447445b69c7b7790b2c5',
                                '5e68448a45b69c7b7790b2c6',
                                '0017be56959511e8b3470016',
                                '001aa40c61c111e8a8a60016',
                                '001ea0984fa111e8a3d40016'],
                          default='5e68447445b69c7b7790b2c5',
                          required=True).data

user_id_in_path = user_id

user_id_in_body = BodyField('uid', 'string', '用户ID', ['5e68447445b69c7b7790b2c5',
                                                     '5e68448a45b69c7b7790b2c6'])

auth = IntegerQueryFiled(name='auth', description="权限级别 ", enum=[1, 2, 10, 11, 12, 13, 14], default=14,
                         required=True).data

auth_in_query = auth

page = IntegerQueryFiled(name='page', description="第几页", enum=[1, 2, 3, 4, 5], default=1).data
size = IntegerQueryFiled(name='size', description="每页条数", enum=[10, 20, 30, 40, 50, 100], default=10).data
page_in_query = page
size_in_query = size

realname_in_body = BodyField('realname', 'string', '用户真名', ['董冬伟'])
username_in_body = BodyField('username', 'string', '用户名', ['Allen7D'])
password_in_body = BodyField('password', 'string', '密码(不输则默认: 123456)', ['123456'])
mobile_in_body = BodyField('mobile', 'string', '手机号', ['13758787058'])
email_in_body = BodyField('email', 'string', '邮箱', ['462870781@qq.com'])
auth_in_body = BodyField('auth', 'integer', '权限(数字: 1,2,10,11,12,13,14,19)', [1, 2, 10, 11, 12, 13, 14, 19])
company_id_in_body = BodyField('company_id', 'string', '公司id', ['5e6784a3d01446cf375d6d37'])