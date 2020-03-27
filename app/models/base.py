# -*- coding: utf-8 -*-
from datetime import datetime

from flask_mongoengine import MongoEngine as _MongoEngine, \
    Document as _Document, DynamicDocument as _DynamicDocument, BaseQuerySet
from flask_mongoengine import create_connections
from app.libs.error_code import NotFound, DuplicateException, RepeatException
from mongoengine import DateTimeField, StringField
from flask_mongoengine.pagination import Pagination
from flask import Flask


class QuerySet(BaseQuerySet):
    def all(self):
        return list(self.__call__())

    def is_exist(self, e=None, error_code=None, msg=None):
        # 是否重复(查找即重复)
        obj = self.first()  #
        if obj:
            _abort_by_error(e)
            raise DuplicateException(error_code=error_code, msg=msg)

    def first_or_404(self, e=None, error_code=None, msg=None):
        '''
        :param e: 异常(exception)
        :param error_code: 错误码
        :param msg: 错误信息
        :return:
        '''
        obj = self.first()
        if obj is None:
            _abort_by_error(e)
            raise NotFound(error_code=error_code, msg=msg)
        return obj

    def all_or_404(self, e=None, error_code=None, msg=None):
        obj = self.all()
        if not obj:
            _abort_by_error(e)
            raise NotFound(error_code=error_code, msg=msg)
        return obj

    def get_or_404(self, *args, **kwargs):
        obj = self.all()
        if not obj:
            raise NotFound()
        return obj

    def paginate_to_package(self, page, per_page, **kwargs):
        rv = self.paginate(page, per_page, **kwargs)
        return {
            'page': page,
            'size': per_page,
            'items': rv.items,
            'total': rv.total,
            'total_page': rv.pages
        }


class Document(_Document):
    meta = {
        'abstract': True,
        'queryset_class': QuerySet,
        # 'allow_inheritance': True
    }


class DynamicDocument(_DynamicDocument):
    meta = {
        'abstract': True,
        'queryset_class': QuerySet,
        # 'allow_inheritance': True
    }


class MongoEngine(_MongoEngine):
    def __init__(self, app=None, config=None):
        super(MongoEngine, self).__init__(app, config)
        self.Document = Document
        self.DynamicDocument = DynamicDocument

        if app is not None:
            self.init_app(app, config)

    def init_app(self, app, config=None):
        if not app or not isinstance(app, Flask):
            raise Exception('Invalid Flask application instance')

        self.app = app

        app.extensions = getattr(app, 'extensions', {})

        if 'mongoengine' not in app.extensions:
            app.extensions['mongoengine'] = {}

        if self in app.extensions['mongoengine']:
            # Raise an exception if extension already initialized as
            # potentially new configuration would not be loaded.
            raise Exception('Extension already initialized')

        if not config:
            # If not passed a config then we read the connection settings
            # from the app config.
            config = app.config

        # Obtain db connection(s)
        connections = create_connections(config)

        # Store objects in application instance so that multiple apps do not
        # end up accessing the same objects.
        s = {'app': app, 'conn': connections}
        app.extensions['mongoengine'][self] = s

    def auto_check_empty(self, e):
        pass


db = MongoEngine()


class CRUDMixin(object):
    """Mixin 添加CRUD操作(create, read, update, delete)."""

    @classmethod
    def get(cls, **kwargs):
        """查"""
        return cls.objects.filter(**kwargs).first()

    @classmethod
    def get_or_404(cls, e=None, error_code=None, msg=None, **kwargs):
        """查，不存在则返回异常"""
        error_kwargs = dict(e=e, error_code=error_code, msg=msg)
        return cls.objects.filter(**kwargs).first_or_404(**error_kwargs)

    @classmethod
    def get_all(cls, **kwargs):
        """查询所有"""
        return cls.objects.filter(**kwargs).all()

    @classmethod
    def is_exist_to_404(cls, e=None, error_code=None, msg=None, **kwargs):
        instance = cls.objects.filter(**kwargs).first()
        if instance:
            _abort_by_error(e)
            raise RepeatException(error_code=error_code, msg=msg)
        else:
            return False

    @classmethod
    def create(cls, **kwargs):
        """增"""
        instance = cls()
        for attr, value in kwargs.items():
            if hasattr(instance, attr) and value is not None:
                setattr(instance, attr, value)
        return instance.save()

    def renew(self, **kwargs):
        """更新"""
        for attr, value in kwargs.items():
            if hasattr(self, attr) and value is not None:
                setattr(self, attr, value)
        return self.save()


class Base(CRUDMixin, Document):
    createdAt = DateTimeField(required=True, default=datetime.now)
    updatedAt = DateTimeField(required=True, default=datetime.now)
    meta = {
        'allow_inheritance': True,
        'abstract': True,
    }

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.exclude = ['createdAt', 'updatedAt', '_cls']
        self.fields = list(set(self._fields_ordered) - set(self.exclude))

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self

    def __getitem__(self, item):
        return getattr(self, item)


def _abort_by_error(e=None):
    if e:
        raise e
