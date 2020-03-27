# -*- coding: utf-8 -*-

from datetime import datetime
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from bson.objectid import ObjectId
from app.libs.error_code import ServerError
import decimal

class JSONEncoder(_JSONEncoder):
    def default(self, o):
        try:
            if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
                return dict(o)
            if isinstance(o, datetime):
                return o.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(o, ObjectId):
                return str(o)
            if isinstance(o, decimal.Decimal):
                return str(o)
        except Exception as e:
            print(e)
            raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder