# -*- coding: utf-8 -*-
from flask import g, current_app
from mongoengine import IntField, StringField, ObjectIdField
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import AuthFailed
from app.libs.scope import Scope
from app.libs.enums import ScopeEnum
from app.models.base import Base
from app.models.group import Group as GroupModel
from app.models.cdkey import CDKey
from app.service.wx_token import WxToken


class User(Base):
    """
    用户表
    """
    username = StringField()  # 账号名
    realname = StringField()  # 真名(便于管理员处理)
    nickname = StringField()  # 微信昵称
    group_id = ObjectIdField()  # 用户所属的权限组id
    _password = StringField(db_field='password')  # 用户密码
    mobile = StringField()  # 手机号
    email = StringField()  # 邮箱
    openid = StringField()  # 微信openid
    company_name = StringField()  # 公司名
    company_id = ObjectIdField()  # 公司ID
    project_name = StringField()  # 项目名
    project_id = ObjectIdField()  # 项目ID
    cdkey = StringField()  # 激活码(用于与微信绑定)
    # auth = IntField(default=1, choices=(1, 2))  # 参考app.libs.enums
    auth = IntField(default=1)  # 1是用户; 2是管理员
    meta = {
        'collection': 'user',
        'strict': True
    }

    def keys(self):
        self.hide('auth', 'openid', '_password').append('auth_scope')
        return self.fields

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @property
    def auth_scope(self):
        try:
            # sys_admin和guest就没有 group_id
            group = GroupModel.objects.filter(id=self.group_id).first()
            if group and group.name:
                return group.name
        except Exception as e:
            if self.auth == 2:
                return '系统超级管理员'
            return '访客'

    @property
    def is_admin(self):
        return ScopeEnum(self.auth) == ScopeEnum.ADMIN

    @staticmethod
    def hash_password(raw):
        password = generate_password_hash(raw)
        return password

    def check_password(self, raw):
        # 单单更新密码
        return check_password_hash(self.password, raw)

    def update_password(self, raw_password):
        self.password = raw_password
        return self

    # 用户名登录
    @staticmethod
    def verify_by_username(username, password):
        user = User.objects.filter(username=username).first_or_404(msg='该用户名未注册')
        if not user.check_password(password):
            raise AuthFailed(msg='密码错误')
        scope = Scope.match_user_scope(auth=user.auth)
        return {'uid': str(user.id), 'scope': scope}

    @staticmethod
    def verify_by_email(email, password):
        user = User.objects.filter(email=email).first_or_404(msg='该邮箱未注册')
        if not user.check_password(password):
            raise AuthFailed(msg='密码错误')
        scope = 1  # Scope.match_user_scope(auth=user.auth)
        return {'uid': str(user.id), 'scope': scope}

    # 手机登录
    @staticmethod
    def verify_by_mobile(mobile, password):
        user = User.objects.filter(mobule=mobile).first_or_404(msg='该手机未注册')
        if not user.check_password(password):
            raise AuthFailed(msg='密码错误')
        scope = Scope.match_user_scope(auth=user.auth)
        return {'uid': str(user.id), 'scope': scope}

    # 微信注册
    @staticmethod
    def register_by_wx_mina(account):
        """小程序注册"""
        guest_group_id = current_app.config['AUTH_GROUPS']['GUEST'].id
        user = User.create(openid=account, group_id=guest_group_id)
        user.save()
        return user

    # 微信登录
    @staticmethod
    def verify_by_wx_mina(code, *args):
        ut = WxToken(code)
        wx_result = ut.get()  # wx_result = {session_key, expires_in, openid}
        openid = wx_result['openid']
        user = User.objects.filter(openid=openid).first()
        # 如果不在数据库，则新建用户
        if not user:
            user = User.register_by_wx_mina(openid)
        scope = Scope.match_user_scope(auth=user.auth)
        return {'uid': str(user.id), 'scope': scope}

    # 用户使用激活吗
    @staticmethod
    def use_cdkey(key, user_id):
        user = User.objects.filter(id=user_id).first_or_404()
        cdkey = CDKey.objects.filter(cdkey=key, activation_state__ne=True).first_or_404()
        CDKey.active_cdkey(key, user_id)
        data = CDKey.verify_hashkey(cdkey["hashkey"])
        user.company_name = data["company_name"]
        user.company_id = data["company_id"]
        user.project_name = data["project_name"]
        user.project_id = data["project_id"]
        user.auth = data["auth"]
        user.save()

    # 获取当前用户
    @classmethod
    def get_current_user(cls):
        return cls.get_or_404(id=g.user.uid)
