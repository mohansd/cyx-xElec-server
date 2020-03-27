# -*- coding: utf-8 -*-
from app.libs.redprint import RedPrint
from app.api_docs.v1 import alarm as api_doc
from flask import request
import datetime
from app.models.alarm import Alarm
from app.libs.error_code import Success
from app.validators.params import PaginateValidator

api = RedPrint(name='alarm', description='告警', api_doc=api_doc)


@api.route('/detail')
def alarm_detail():
    """
    根据alarm_id查询告警详情
    :return:
    """
    alarm_id = request.args.get('alarm_id')
    alarm = Alarm.objects.filter(id=alarm_id).first()
    return Success(alarm)


@api.route('/check', methods=['POST'])
def check_alarm():
    """
    根据alarm_id 将告警更新成已读
    :return:
    """
    alarm_id = request.get_json()["alarm_id"]
    alarm = Alarm.objects.filter(id=alarm_id).first()
    alarm.status = 1
    alarm.save()
    return Success()


@api.route('/project', methods=['POST'])
def project_alarm():
    """
    返回项目下所有的告警信息
    :return:
    """
    filter = {}
    data = request.get_json()
    validator = PaginateValidator().validate_for_api()
    page, size = validator.page.data, validator.size.data
    for key, value in data.items():
        if key == "start":
            filter["createdAt__gte"] = datetime.datetime.fromtimestamp(value)
        elif key == "end":
            filter["createdAt__lte"] = datetime.datetime.fromtimestamp(value)
        elif key == "sort":
            continue
        else:
            filter[key] = value
    alarms = Alarm.objects(**filter)
    alarms = alarms.filter().order_by(*data["sort"]).paginate_to_package(page=page, per_page=size)
    return Success(alarms)
