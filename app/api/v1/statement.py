# -*- coding: utf-8 -*-

from app.libs.redprint import RedPrint
from app.api_docs.v1 import statement as api_doc
from app.models.monitor import Monitor
from app.models.line import Line
from app.models.alarm import Alarm
from app.models.device import Device
from app.models.statistics_hour import StatisticsHour
from app.libs.utils import zero_time, month_datetime
from app.libs.error_code import Success
from app.libs.schedule_task import energy_avg_statistics
from flask import request
from bson.objectid import ObjectId

api = RedPrint(name='statement', description='报表', api_doc=api_doc)


@api.route('/today/electricity')
def device_today_electricity():
    """
    当日电流趋势
    :return:
    """

    if "device_id" in request.args:
        result = []
        device_id = request.args.get("device_id")
        lines = Line.objects.filter(device_id=device_id).all()
        for line in lines:
            monitor = Monitor.objects.filter(createdAt__gte=zero_time(), line_id=line.id, type="electricity").order_by(
                "+createdAt").all()
            data = []
            for mt in monitor:
                data.append({
                    "time": mt.createdAt,
                    "value": {
                        "a": mt.value["a"],
                        "b": mt.value["b"],
                        "c": mt.value["c"],
                        "total": round(mt.value["a"] + mt.value["b"] + mt.value["c"], 2)
                    }
                })
            result.append({
                "line_id": line.id,
                "line": line.line,
                "line_name": line.line_name,
                "data": data
            })
        return Success(result)
    if "line_id" in request.args:
        result = {}
        line_id = request.args.get("line_id")
        line = Line.objects.filter(id=line_id).first()
        monitor = Monitor.objects.filter(createdAt__gte=zero_time(), line_id=line.id, type="electricity").order_by(
            "+createdAt").all()
        data = []
        for mt in monitor:
            data.append({
                "time": mt.createdAt,
                "value": {
                    "a": mt.value["a"],
                    "b": mt.value["b"],
                    "c": mt.value["c"],
                    "total": round(mt.value["a"] + mt.value["b"] + mt.value["c"], 2)
                }
            })
        result["data"] = data
        result["line_id"] = line.id
        result["line_name"] = line.line_name
        result["line"] = line.line
        return Success(result)


@api.route('/today/energy')
def device_today_energy():
    """
    当日电能趋势
    :return:
    """
    if "device_id" in request.args:
        device_id = request.args.get('device_id')
        result = []
        lines = Line.objects.filter(device_id=device_id).all()
        for line in lines:
            hour_energy = StatisticsHour.objects.filter(zero_time=zero_time(), line_id=line.id).order_by(
                "+createdAt").all()
            data = []
            for e in hour_energy:
                data.append({
                    "time": e.hour_time,
                    "value": e.energy
                })
            result.append({
                "line": line.line,
                "line_name": line.line_name,
                "line_id": line.id,
                "data": data
            })
        return Success(result)
    if "line_id" in request.args:
        line_id = request.args.get('line_id')
        line = Line.objects.filter(id=line_id).first()
        result = {}
        hour_energy = StatisticsHour.objects.filter(zero_time=zero_time(), line_id=line.id).order_by("+createdAt").all()
        data = []
        for e in hour_energy:
            data.append({
                "time": e.hour_time,
                "value": e.energy
            })
        result["data"] = data
        result["line_id"] = line.id
        result["line_name"] = line.line_name
        result["line"] = line.line
        return Success(result)



@api.route('/today/energy_add')
def device_today_energy_add():
    """
    当日电能累计
    :return:
    """
    device_id = request.args.get('device_id')
    result = []
    lines = Line.objects.filter(device_id=device_id).all()
    for line in lines:
        max_energy = Monitor.objects.filter(createdAt__gte=zero_time(), line_id=line.id, type="energy").order_by(
            "-createdAt").first()
        min_energy = Monitor.objects.filter(createdAt__gte=zero_time(), line_id=line.id, type="energy").order_by(
            "+createdAt").first()
        if min_energy and min_energy:
            energy = max_energy["value"] - min_energy["value"]
        else:
            energy = 0
        result.append({
            "line": line.line,
            "line_name": line.line_name,
            "energy": energy
        })
    return Success(result)


@api.route('/month/energy_add')
def device_month_erergy_add():
    """
    当月电能累计
    :return:
    """
    device_id = request.args.get('device_id')
    result = []
    lines = Line.objects.filter(device_id=device_id).all()
    for line in lines:
        max_energy = Monitor.objects.filter(createdAt__gte=month_datetime(), line_id=line.id, type="energy").order_by(
            "-createdAt").first()
        min_energy = Monitor.objects.filter(createdAt__gte=month_datetime(), line_id=line.id, type="energy").order_by(
            "+createdAt").first()
        if min_energy and min_energy:
            energy = max_energy["value"] - min_energy["value"]
        else:
            energy = 0
        result.append({
            "line": line.line,
            "line_name": line.line_name,
            "energy": energy,
            "line_id": line.id
        })
    return Success(result)


@api.route('/test')
def test():
    # match = {"$match": {"line_id": ObjectId("5e6ee2f7c1094a4d94ed0266")}}
    # group = {"$group": {"_id": {"$hour": "$hour_time"}, "energy": {"$avg": "$energy"}}}
    # sort = {"$sort": {"_id": 1}}
    # test = StatisticsHour.objects.aggregate(*[match, group, sort])
    # print(list(test))
    # print(type(test))
    # return Success(test)
    energy_avg_statistics()
    return Success()


@api.route('/device')
def device_detail_statement():
    device_id = request.args.get('device_id')
    device = Device.objects.filter(device_id=device_id).first()
    lines = Line.objects.filter(device_id=device_id).all()
    trip_count = Alarm.objects.filter(device_id=device_id, alarm_type="trip").count()
    breakpoint = []
    line_detail = []
    for line in lines:
        if line.line == 0:
            continue
        monitor = Monitor.objects.filter(type="status", value__status="off").order_by("-createdAt").first()
        if monitor:
            breakpoint.append({
                "line_name": line.line_name,
                "last_time": monitor.createdAt
            })

        max_energy = Monitor.objects.filter(createdAt__gte=zero_time(), line_id=line.id, type="energy").order_by(
            "-createdAt").first()
        min_energy = Monitor.objects.filter(createdAt__gte=zero_time(), line_id=line.id, type="energy").order_by(
            "+createdAt").first()
        if min_energy and min_energy:
            energy = max_energy["value"] - min_energy["value"]
        else:
            energy = 0
        line_detail.append({
            "line": line.line,
            "line_name": line.line_name,
            "energy": energy
        })

    location = device.location
    category = device.category_name
    result = {
        "online_time": 10,
        "power_on_time": 10,
        "breakpoint": breakpoint,
        "category": category,
        "location": location,
        "trip_count": trip_count,
        "line_detail": line_detail
    }
    return Success(result)


