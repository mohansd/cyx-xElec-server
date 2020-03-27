# _*_ coding: utf-8 _*_

from app.libs.swagger_filed import IntegerQueryFiled, StringQueryFiled, StringPathFiled, BodyField

uid = StringPathFiled(name='uid',
                      description="用户ID",
                      enum=['5e68447445b69c7b7790b2c5',
                            '5e68448a45b69c7b7790b2c6',
                            '5e68448a45b69c7b7791b2c6',
                            'xxxxxxxxxxxxxxxxxxxxxxxx'
                            ],
                      default='5e68447445b69c7b7790b2c5',
                      required=True)

auth = IntegerQueryFiled(name='auth', description="权限级别 ", enum=[1, 2, 10, 11, 12, 13, 14], default=14,
                         required=True)

realname_in_body = BodyField('realname', 'string', '用户真名', ['董冬伟'])
username_in_body = BodyField('username', 'string', '用户名', ['Allen7D'])
password_in_body = BodyField('password', 'string', '密码(不输则默认: 123456)', ['123456'])
mobile_in_body = BodyField('mobile', 'string', '手机号', ['13758787058'])
email_in_body = BodyField('email', 'string', '邮箱', ['462870781@qq.com'])
auth_in_body = BodyField('auth', 'integer', '权限(数字: 1,2,10,11,12,13,14,19)', [1, 2, 10, 11, 12, 13, 14, 19])

company_id_in_query = StringQueryFiled(name='company_id',
                                       description="公司ID",
                                       enum=['5e6784a3d01446cf375d6d37',
                                             '5e6784afd01446cf375d6d38'],
                                       default='5e6784a3d01446cf375d6d37',
                                       required=True)
company_id_in_body = BodyField('company_id', 'string', '公司id',
                              [
                                  '5e6784a3d01446cf375d6d37',
                                  '5e6784afd01446cf375d6d38'
                              ]
                              )
