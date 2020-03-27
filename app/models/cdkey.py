# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import StringField, DateTimeField, BooleanField, ObjectIdField, BinaryField, IntField
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app

from app.libs.utils import generate_uuid
from app.libs.error_code import AuthFailed
from app.models.group import Group as GroupModel
from app.models.project import Project as ProjectModel
from .base import Base


class CDKey(Base):
    """，，，，，
    激活码表
    不用在乎激活码是谁生成的，而是哪个公司生成的。因为genUser会变
    激活码为啥要知道是被谁激活的？

    激活码：公司信息
    """
    cdkey = StringField()  # cdkey为较短的控制在8-16位， 可以用uuid生成
    hashkey = BinaryField()  # hashkey和cdkey保持对应 可以解析为真实信息
    gen_user = ObjectIdField()  # 生成者ID(便于生成者管理)
    auth = IntField(default=20, choices=(1, 2, 10, 11, 12, 13, 14, 20))  # 参考app.libs.enums
    group_id = ObjectIdField()  # 项目组ID
    company_id = ObjectIdField()  # 公司ID
    project_id = ObjectIdField()  # 项目ID
    active_user = ObjectIdField()  # 激活用户ID(该字段不用；因为很多人会用)
    active_time = DateTimeField()  # 激活时间(该字段不用)
    expired_time = DateTimeField()  # 失效时间
    state = BooleanField(default=True)  # 激活状态(True:有效,False:失效)
    meta = {
        'collection': 'cdkey',
        'strict': True
    }

    def keys(self):
        self.append('group_name', 'project_name')
        return self.fields

    @property
    def group_name(self):
        try:
            group = GroupModel.get_or_404(id=self.group_id)
            return group.name
        except Exception:
            return ''

    @property
    def project_name(self):
        try:
            project = ProjectModel.get_or_404(id=self.project_id)
            return project.name
        except Exception:
            return ''

    # 生成hashkey
    @staticmethod
    def generate_hashkey(company_name, company_id, auth, group_id, project_name='', project_id=''):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({
            'company_name': company_name,
            'company_id': company_id,
            'auth': auth,
            'group_id': group_id,
            'project_name': project_name,
            'project_id': project_id
        })

    @staticmethod
    def generate_cdkey():
        # 生成cdkey
        return generate_uuid()[0:8].upper()

    @staticmethod
    def verify_hashkey(hashkey):
        # 解析hashkey
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(hashkey)
        except BadSignature:
            raise AuthFailed(msg='激活码失效', error_code=1002)
        except SignatureExpired:
            raise AuthFailed(msg='激活码过期', error_code=1003)
        return data

    # 存储生成的cdkey
    @staticmethod
    def save_cdkey(uid, hashkey, cdkey, auth, group_id, company_id, project_id=''):
        create_condition = \
            dict(cdkey=cdkey, hashkey=hashkey, gen_user=uid,
                 auth=auth, group_id=group_id, company_id=company_id,
                 project_id=project_id) \
                if project_id else \
                dict(cdkey=cdkey, hashkey=hashkey, gen_user=uid, auth=auth,
                     group_id=group_id, company_id=company_id)

        cdkey = CDKey(**create_condition)
        cdkey.save()
        return cdkey

    # 激活cdkey
    @staticmethod
    def active_cdkey(key, uid):
        cdkey = CDKey.objects.filter(cdkey=key).first_or_404()
        cdkey.active_user = uid
        cdkey.active_time = datetime.now()
        cdkey.save()

    @classmethod
    def toggle_state(cls, cdkey, state):
        cdkey_obj = cls.objects.filter(cdkey=cdkey).first_or_404()
        cdkey_obj.state = True if state else False
        cdkey_obj.save()
