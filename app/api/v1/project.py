# -*- coding: utf-8 -*-

from app.libs.redprint import RedPrint
from app.api_docs.v1 import project as api_doc
from app.models.user import User
from app.models.device import Device
from app.models.project import Project
from app.models.company import Company
from app.models.alarm import Alarm
from flask import request
from app.libs.error_code import Success
import datetime

api = RedPrint(name='project', description='项目', api_doc=api_doc)


@api.route('/list')
def project_list():
    """
    返回公司下的项目列表
    :return:
    """
    project = Project.objects.all(companyName="金峰测试")
    return Success(list(project))


@api.route('/add', methods=['POST'])
def add_project():
    """
    添加公司项目
    :return:
    """
    data = request.get_json()
    print(data)
    project = Project()
    project["name"] = data["project_name"]
    company_name = "金峰测试"
    company = Company.objects.filter(name=company_name).first_or_404()
    project["company_id"] = company["id"]
    project.save()
    for device_id in data["device"]:
        device = Device.objects.filter(device_id=device_id).first_or_404()
        device["project_name"] = data["project_name"]
        device["project_id"] = project["id"]
        device.save()
    return Success()


@api.route('/edit',methods=['POST'])
def edit_project():
    """
    编辑项目
    :return:
    """
    data = request.get_json()
    project = Project.objects.filter(id=data["project_id"]).first_or_404()
    devices = Device.objects.filter(project_name=project["name"]).get_or_404()
    for device in devices:
        device["project_name"] = data["project_name"]
        device.save()
    project["name"] = data["project_name"]
    project.save()
    return Success()


@api.route('/delete',methods=['POST'])
def delete_project():
    """
    删除项目
    :return:
    """
    data = request.get_json()
    project_id = data["project_id"]
    project = Project.objects.filter(id=project_id).first_or_404()
    project.delete()
    devices = Device.objects.filter(project_id=project_id).get_or_404()
    for device in devices:
        device["project_id"] = None
        device["project_name"] = None
        device.save()
    return Success()


@api.route('/remove/device', methods=['POST'])
def remove_device():
    """
    将设备从项目中移除
    :return:
    """
    data = request.get_json()
    device_id = data["device_id"]
    device = Device.objects.filter(device_id=device_id).first_or_404()
    device["project_name"] = None
    device["project_id"] = None
    device.save()
    return Success()

@api.route('/add/device', methods=['POST'])
def add_device():
    """
    项目添加设备
    :return:
    """
    data = request.get_json()
    device = Device.objects(__raw__={"project_id":{"$exists":False},"device_id":data["device_id"]}).first_or_404()
    project = Project.objects.filter(id=data["project_id"]).first_or_404()
    device["project_id"] = project["id"]
    device["project_name"] = project["name"]
    device.save()
    return Success()
