# _*_ coding: utf-8 _*_
"""

"""
from app.libs.swagger_filed import IntegerQueryFiled, IntegerPathFiled, StringPathFiled, StringQueryFiled, BodyField

__author__ = 'Allen7D'

page_in_query = IntegerQueryFiled(name='page', description="第几页", enum=[1, 2, 3, 4, 5], default=1)
size_in_query = IntegerQueryFiled(name='size', description="每页大小", enum=[10, 20, 30, 40, 50, 100], default=10)

# User
uid_in_path = StringPathFiled(name='uid',
                              description="用户ID",
                              enum=['5e68447445b69c7b7790b2c5',
                                    '5e68448a45b69c7b7790b2c6',
                                    '5e68448a45b69c7b7791b2c6',
                                    '5e705d50e3a1dff793a99b6d',
                                    'xxxxxxxxxxxxxxxxxxxxxxxx'
                                    ],
                              default='5e68447445b69c7b7790b2c5',
                              required=True)
realname_in_body = BodyField('realname', 'string', '用户真名', ['董冬伟'])
username_in_body = BodyField('username', 'string', '用户名', ['Allen7D'])
password_in_body = BodyField('password', 'string', '密码(不输则默认: 123456)', ['123456'])
mobile_in_body = BodyField('mobile', 'string', '手机号', ['13758787058'])
email_in_body = BodyField('email', 'string', '邮箱', ['462870781@qq.com'])
auth_in_body = BodyField('auth', 'integer', '权限等级(数字: 1,2,10,11,12,13,14,20,999)', [1, 2, 10, 11, 12, 13, 14, 20, 999])

#  CDKey
cdkey_in_path = StringPathFiled(name='cdkey',
                                description="CDKey(激活码)",
                                enum=['E2E058B2',
                                      'D4E513E3',
                                      '7F5FBC0B'
                                      ],
                                default='E2E058B2',
                                required=True)
cdkey_in_query = StringQueryFiled(name='cdkey',
                                  description="CDKey(激活码)",
                                  enum=['E2E058B2',
                                        'D4E513E3',
                                        '7F5FBC0B'
                                        ],
                                  default='E2E058B2',
                                  required=True)

company_id_in_path = StringPathFiled(name='id',
                                     description="公司ID",
                                     enum=['5e6784a3d01446cf375d6d37',
                                           '5e6784afd01446cf375d6d38'
                                           ],
                                     default='5e6784a3d01446cf375d6d37',
                                     required=True)
company_id_in_query = StringQueryFiled(name='company_id',
                                       description="公司ID",
                                       enum=['5e6784a3d01446cf375d6d37',
                                             '5e6784afd01446cf375d6d38'
                                             ],
                                       default='5e6784a3d01446cf375d6d37',
                                       required=True)
company_id_in_body = BodyField(
    'company_id', 'string', '公司ID',
    [
        '5e6784a3d01446cf375d6d37',
        '5e6784afd01446cf375d6d38'
    ]
)
company_name_in_body = BodyField('company_name', 'string', '公司名', ["杭州嗨皮有限公司", "杭州哈哈有限公司"])

# Project
project_name_in_body = BodyField('project_name', 'string', '项目名', ["金峰"])

project_id_in_body = BodyField('project_id', 'string', '项目ID',
                               [
                                   '5e6784a3d01446cf375d6d37',
                                   '5e6784afd01446cf375d6d38'
                               ]
                               )

project_id_in_path = StringPathFiled(name='project_id',
                                     description="项目ID",
                                     enum=['5e6784a3d01446cf375d6d37',
                                           '5e6784afd01446cf375d6d38'
                                           ],
                                     default='5e6784a3d01446cf375d6d37',
                                     required=True)
project_id_in_path = StringQueryFiled(name='project_id',
                                      description="项目ID",
                                      enum=['5e6784a3d01446cf375d6d37',
                                            '5e6784afd01446cf375d6d38'
                                            ],
                                      default='5e6784a3d01446cf375d6d37',
                                      required=True)

# 权限组
group_id_in_path = StringPathFiled(
    name='group_id', description="权限组ID", enum=['1', '2', '3', '4', '5', '10', '15', '20'], required=True)
group_id_in_query = StringQueryFiled(
    name='group_id', description="权限组ID", enum=['1', '2', '3', '4', '5', '10', '15', '20'], required=True)
group_id_in_body = BodyField(
    name='group_id', type='string', description="权限组ID", enum=['1', '2', '3', '4', '5', '10', '15', '20'])

# 权限
auth_ids_in_body = BodyField(name='auth_ids', type='array', description='权限ID列表',
                             enum=[[6, 7, 8], [12, 13, 14]])

# User
nickname_in_body = BodyField(name='nickname', type='string', description='昵称', enum=['Allen7D'])
email_in_body = BodyField(name='email', type='string', description='邮箱', enum=['462870781@qq.com'])
mobile_in_body = BodyField(name='mobile', type='string', description='手机', enum=['13758787058'])

# Password
new_password_in_body = BodyField('new_password', 'string', '密码(不输则默认: 123456)', ['123456'])
confirm_password_in_body = BodyField('confirm_password', 'string', '密码(不输则默认: 123456)', ['123456'])