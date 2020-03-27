# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/3/19.
  用户激活
"""
from app.models.company import Company as CompanyModel
from app.models.project import Project as ProjectModel
from app.models.user import User as UserModel
__author__ = 'Allen7D'

class UserActive():
    def __init__(self):
        pass

    @staticmethod
    def active_co_super_or_admin(cdkey, uid, username='', realname='', password='123456', mobile='', email=''):
        company_id = cdkey.company_id
        company = CompanyModel.objects.filter(id=company_id).first_or_404()
        company.manager_name = username
        company.manager_id = uid
        company.cdkey = cdkey.cdkey

        user = UserModel.objects.filter(id=uid).first_or_404()
        user.username = username
        user.realname = realname
        user.password = password
        user.mobile = mobile
        user.email = email
        user.company_name = company.name
        user.company_id = company.id
        user.cdkey = cdkey.cdkey
        user.group_id = cdkey.group_id # 用户权限

        user.save()
        company.save()

    @staticmethod
    def active_co_employee(cdkey, uid, username='', realname='', password='123456', mobile='', email=''):
        company = CompanyModel.objects.filter(id=cdkey.company_id).first_or_404()
        company.manager_name = username
        company.manager_id = uid
        company.cdkey = cdkey.cdkey

        user = UserModel.objects.filter(id=uid).first_or_404()
        user.username = realname
        user.realname = realname
        user.password = password
        user.mobile = mobile
        user.email = email
        user.cdkey = cdkey.cdkey
        user.group_id = cdkey.group_id # 用户权限
        # 将公司信息录入到用户
        user.company_name = company.name
        user.company_id = company.id
        # 将项目信息录入到用户
        project = ProjectModel.objects.filter(id=cdkey.project_id).first_or_404()
        user.project_id = project.id
        user.project_name = project.name

        user.save()
        company.save()