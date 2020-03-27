# -*- coding: utf-8 -*-
import time

from flask import current_app
from flask.json import dumps
from uuid import uuid4
from binascii import a2b_hex, b2a_hex
import datetime

def jsonify(*args, **kwargs):
    indent = None
    separators = (",", ":")

    if current_app.config["JSONIFY_PRETTYPRINT_REGULAR"] or current_app.debug:
        indent = 2
        separators = (", ", ": ")

    if args and kwargs:
        raise TypeError("jsonify() behavior undefined when passed both args and kwargs")
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs
    return current_app.response_class(
        dumps(data, indent=indent, separators=separators) + "\n",
        mimetype=current_app.config["JSONIFY_MIMETYPE"],
    ).json


def generate_uuid():
    uid = str(uuid4())
    return ''.join(uid.split('-'))


def dynamic_decimal(data):
    if int(data) >= 100:
        data = int(data)
    else:
        data = round(data, 1)
    return data


def command_encode(command):
    return a2b_hex(command)


def data_decode(data):
    return str(b2a_hex(data)).upper()[2:-1]


def multiple_run(number, func, args=(), sleep=None):
    for number in range(0, number):
        func(*args)
        if sleep:
            time.sleep(sleep)


def test_job(device_id, line_id, operate, plan_id):
    print(datetime.datetime.now().strftime('%H:%M:%S') + "device_id:" + str(device_id) + "line_id:" + str(line_id) + "type:" + operate + "plan_id" + str(plan_id))


def month_datetime():
    this_month = datetime.datetime(datetime.date.today().year, datetime.date.today().month, 1)
    return this_month

def zero_time():
    today = datetime.datetime.today()
    day_time = datetime.datetime(year=today.year, month=today.month, day=today.day)
    return day_time

def last_month_datetime():
    this_month = month_datetime()
    month = (this_month - datetime.timedelta(days=1)).month
    year = (this_month - datetime.timedelta(days=1)).year
    last_month = datetime.datetime(year, month, 1)
    return last_month

