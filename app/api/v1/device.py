# -*- coding: utf-8 -*-
import time
import traceback

from app.libs.redprint import RedPrint
import random
from app.api_docs.v1 import device as api_doc
from flask import request
from app.models.device import Device
from app.models.project import Project
from app.models.monitor import Monitor
from app.models.line import Line
from app.models.alarm import Alarm
from app.models.load_type import LoadType

from app.libs.error_code import Success, NotFound, DeviceException
from app.libs.utils import zero_time
from app.service import socketservice
from app.service.device import Device as Deviceservice
from app.libs.utils import jsonify, multiple_run, month_datetime
import decimal

api = RedPrint(name='device', description='设备', api_doc=api_doc)


@api.route('/all')
def device_all_list():
    """
    所有设备的项目列表
    :return:
    """
    device = Device.objects.filter(company_name="金峰测试").get_or_404()
    return Success(list(device))


@api.route('/unused/list')
def unused_device_list():
    """
    未选择项目的设备列表
    :return:
    """
    # companyId = request.args.get("companyId",'')
    devices = Device.objects(__raw__={"project_id": None, "company_name": "金峰测试"}).get_or_404()
    return Success(list(devices))


@api.route('/used/list')
def used_device_list():
    """
    已选择项目的设备列表
    :return:
    """
    # companyId = request.args.get("companyId")
    devices = Device.objects.filter(__raw__={"project_id": {"$exists": True}, "company_name": "金峰测试"}).get_or_404()
    return Success(list(devices))


@api.route('/list')
def device_list():
    """
    公司项目组详情列表
    包括项目名、设备列表、告警数、设备在线数
    :return:
    """
    project = Project.objects(company_name="金峰测试").all()
    data = []
    for p in project:
        print(p["name"])
        device = Device.objects(project_id=p["id"]).all()
        print(device)
        online = Project.get_online_number(p["id"])
        alarm_count = Alarm.objects.filter(project_id=p["id"], createdAt__gte=month_datetime(), status=0).count()
        data.append({
            "project_name": p["name"],
            "project_id": p["id"],
            "device_list": list(device),
            "device_number": len(device),
            "online": online,
            "alarm_count": alarm_count
        })
    return Success(data)


@api.route('/project')
def project_device_list():
    """
    项目设备列表
    :return:
    """
    data = request.args.get("project")
    device = Device.objects.filter(project_id=data).get_or_404()
    return Success(list(device))


# 预留
@api.route('/add', methods=['POST'])
def add_device():
    pass


@api.route('/edit', methods=['POST'])
def edit_device():
    """编辑设备信息"""
    data = request.get_json()
    device = Device.objects.filter(device_id=data["device_id"]).first_or_404()
    device["alias"] = data["alias"]
    device["location"] = data["location"]
    device["electricity"] = decimal.Decimal(data["electricity"])
    device.save()
    return Success()


# 操控线路
@api.route('', methods=['POST'])
def operate_device():
    """
    操控设备线路
    :return:
    """
    data = request.get_json()
    device_id = data["device_id"]
    socket = Deviceservice.search_device_socket(device_id)
    multiple_run(3, Deviceservice.operate, args=(data["line"], data["type"], socket), sleep=0.5)
    return Success()


@api.route('/status')
def device_status():
    """
    设备状态详细信息
    :return:
    """
    project_id = request.args.get("project_id")
    devices = list(Device.objects.filter(project_id=project_id).all())
    clients = socketservice.get_instance().clients
    result = []
    for device in devices:
        monitor_energy_max = Monitor.objects.filter(device_id=device["device_id"], line=0, type="energy",
                                                    createdAt__gte=zero_time()).order_by('-createdAt').first()
        monitor_energy_min = Monitor.objects.filter(device_id=device["device_id"], line=0, type="energy",
                                                     createdAt__gte=zero_time()).order_by('+createdAt').first()
        monitor_electricity = Monitor.objects.filter(device_id=device["device_id"], line=0, type="electricity").first()
        energy = monitor_energy_max.value - monitor_energy_min.value if monitor_energy_max else None
        electricity = monitor_electricity.value if monitor_electricity else None
        cloud_id = device["cloud_id"]
        data = jsonify(device)
        data["energy"] = energy
        data["electricity"] = electricity
        data["alarm_count"] = Alarm.objects.filter(device_id=device["device_id"], createdAt__gte=month_datetime(),
                                                   status=0).count()
        if device["cloud_id"] in clients.keys():
            socket = clients[cloud_id]
            data["online"] = True
            data["sign"] = socket.sign
            result.append(data)
        else:
            data["online"] = False
            data["sign"] = None
            result.append(data)
    return Success(result)


@api.route('/test')
def test():
    clients = socketservice.get_instance().clients
    print(clients)
    socket = clients["28181101638EEF57"]
    Deviceservice.get_box_detail(socket)
    return Success()


@api.route('/detail')
def device_detail():
    """
    设备详情
    :return:
    """
    device_id = request.args.get("device_id")
    device = Device.objects.filter(device_id=device_id).first_or_404()
    return Success(device)


@api.route('/line')
def line_status():
    """
    设备线路详情
    :return:
    """
    device_id = request.args.get("device_id")
    lines = Line.objects(device_id=device_id).all()
    result = Monitor.device_status(device_id, lines)
    result.pop(0)
    return Success(result)


@api.route('/command')
def send_command():
    """
    发送指令
    :return:
    """
    device_id = request.args.get("device_id")
    command = request.args.get("command")
    socket = Deviceservice.search_device_socket(device_id)
    Deviceservice.send_command(socket, command)
    return Success(msg="指令发送成功")


@api.route('/update')
def update_device():
    """
    更新设备线路状态，发送指令获取设备状态
    :return:
    """
    device_id = request.args.get("device_id")
    socket = Deviceservice.search_device_socket(device_id)
    Deviceservice.update_device(socket)
    return Success(msg="指令发送成功")


@api.route('/load_type', methods=['POST', 'GET'])
def create_load_type():
    if request.method == 'POST':
        data = request.get_json()
        LoadType.create(**data)
        return Success()
    else:
        load_type = LoadType.objects.all()
        return Success(load_type)


@api.route('/choice/load_type', methods=['POST'])
def line_choice_load_type():
    data = request.get_json()
    line = Line.objects.filter(id=data["line_id"]).first()
    line.load_type_id = data["load_type_id"]
    line.save()
    return Success()


@api.route('/load_type/delete', methods=['POST'])
def delete_load_type():
    data = request.get_json()
    load_type = LoadType.objects.filter(id=data["load_type_id"]).first()
    lines = Line.objects.filter(load_type_id=data["load_type_id"]).all()
    load_type.delete()
    if lines:
        for line in lines:
            line.load_type_id = None
            line.save()
    return Success()


@api.route('/asset')
def device_asset():
    devices = Device.objects.filter(company_name="金峰测试").all()
    devices = [device.hide('category_id', 'cloud_id', 'company_id', 'icc_id', 'id') for device in devices]
    return Success(list(devices))
