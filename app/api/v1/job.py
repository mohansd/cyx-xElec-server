# -*- coding: utf-8 -*-
from app.libs.redprint import RedPrint
from app.api_docs.v1 import job as api_doc
from app.models.plan import Plan
from app.models.line import Line
from app.models.job import Job
from flask import request
from app.libs.error_code import Success
from app.service.scheduler import APScheduler
from app.libs.utils import jsonify

api = RedPrint(name='job', description='送电计划', api_doc=api_doc)


@api.route('/list')
def job_list():
    """
    根据项目id返回计划列表
    :return:[{
            "count": 1,
            "id": "5e71dd0d3ae156497e114364",
            "off": [
                {
                    "hour": "12",
                    "minute": "05"
                }
            ],
            "on": [
                {
                    "hour": "17",
                    "minute": "01"
                }
            ],
            "plan_name": "测试计划1",
            "project_id": "5e69f8311366ea889c7cff4c"
        }]
    """
    project_id = request.args.get("project_id")
    plans = jsonify(list(Plan.objects.filter(project_id=project_id).all()))
    for plan in plans:
        count = Line.objects.filter(choice_plan=plan["id"]).count()
        plan["count"] = count
    return Success(plans)


@api.route('/add', methods=['POST'])
def add_job():
    """
    添加任务
    body参数: plan_name on off project_id
    :return:
    """
    data = request.get_json()
    Plan(plan_name=data["plan_name"], on=data["on"], off=data["off"], project_id=data["project_id"]).save()
    return Success()


@api.route('/choice/plan', methods=['POST'])
def choice_job():
    """
    选择配电计划并初始化定时任务，初始化任务后暂停
    body参数 plan_id line_id
    :return:
    """
    data = request.get_json()
    plan = Plan.objects.filter(id=data["plan_id"]).first_or_404()
    line = Line.objects.filter(id=data["line_id"]).first_or_404()
    if line.choice_plan is not None:
        return Success(msg="任务已存在")
    line.choice_plan = data["plan_id"]
    line.plan_status = False
    scheduler = APScheduler()
    scheduler.init_job(on=plan.on, off=plan.off, line=line)
    line.save()
    return Success()


@api.route('/start', methods=['POST'])
def start_job():
    """
    启用计划
    body参数 line_id
    :return:
    """
    data = request.get_json()
    line_id = data["line_id"]
    line = Line.objects.filter(id=line_id).first_or_404()
    jobs = Job.objects.filter(line_id=line_id).get_or_404()
    for job in jobs:
        job_id = job.job_id
        scheduler = APScheduler()
        scheduler.resume_job(job_id=job_id)
    line.plan_status = True
    line.save()
    return Success()


@api.route('/stop', methods=['POST'])
def stop_job():
    """
    暂停计划
    body参数 line_id
    :return:
    """
    data = request.get_json()
    line_id = data["line_id"]
    line = Line.objects.filter(id=line_id).first_or_404()
    jobs = Job.objects.filter(line_id=line_id).get_or_404()
    for job in jobs:
        job_id = job.job_id
        scheduler = APScheduler()
        scheduler.pause_job(job_id=job_id)
    line.plan_status = False
    line.save()
    return Success()


@api.route('/change', methods=['POST'])
def change_job():
    """
    更换计划 删除已配置的定时任务，选择计划后重新初始化定时任务
    body参数 line_id plan_id
    :return:
    """
    data = request.get_json()
    line_id = data["line_id"]
    line = Line.objects.filter(id=line_id).first_or_404()
    jobs = Job.objects.filter(line_id=line_id).all()
    print(jobs)
    for job in jobs:
        job_id = job.job_id
        scheduler = APScheduler()
        scheduler.remove_job(job_id=job_id)
        job.delete()
    plan = Plan.objects.filter(id=data["plan_id"]).first_or_404()
    line.choice_plan = data["plan_id"]
    line.plan_status = False
    scheduler = APScheduler()
    scheduler.init_job(on=plan.on, off=plan.off, line=line, plan_id=plan.id)
    line.save()
    return Success()


@api.route('/delete', methods=['POST'])
def delete_plan():
    """
    删除计划，并直接移除定时任务
    :return:
    """
    data = request.get_json()
    plan_id = data["plan_id"]
    plan = Plan.objects.filter(id=plan_id).first_or_404()
    plan.delete()
    jobs = Job.objects.filter(plan_id=plan_id).all()
    for job in jobs:
        job_id = job.job_id
        scheduler = APScheduler()
        scheduler.remove_job(job_id=job_id)
        job.delete()
    lines = Line.objects.filter(choice_plan=plan_id).all()
    for line in lines:
        line.choice_plan = None
        line.plan_status = None
        line.save()
    return Success()


@api.route('/line')
def line_job():
    """
    每条线路的计划分配情况
    :return: "data": [
        {
            "choice_plan": "5e71dd0d3ae156497e114364",
            "device_id": "7WIZya2wsIKGuitNpHyIWjCq",
            "id": "5e6ee2ddc1094a4d94ed0264",
            "limit": 100.0,
            "line": 1,
            "line_name": "线路一",
            "off": [
                {
                    "hour": "12",
                    "minute": "05"
                }
            ],
            "on": [
                {
                    "hour": "17",
                    "minute": "01"
                }
            ],
            "plan_name": "测试计划1",
            "plan_status": false,
            "standard": 78
        },
        {
            "choice_plan": null,
            "device_id": "7WIZya2wsIKGuitNpHyIWjCq",
            "id": "5e6ee2e8c1094a4d94ed0265",
            "limit": 160.0,
            "line": 2,
            "line_name": "线路二",
            "plan_status": null,
            "standard": 78
        },
        {
            "choice_plan": null,
            "device_id": "7WIZya2wsIKGuitNpHyIWjCq",
            "id": "5e6ee2f7c1094a4d94ed0266",
            "limit": 250.0,
            "line": 3,
            "line_name": "线路三",
            "plan_status": null,
            "standard": 78
        }
    ]
    """
    device_id = request.args.get("device_id")
    lines = jsonify(list(Line.objects.filter(device_id=device_id).get_or_404()))
    result = []
    for line in lines:
        if line["choice_plan"]:
            plan = Plan.objects.filter(id=line["choice_plan"]).first()
            if plan:
                line["plan_name"] = plan["plan_name"]
                line["on"] = plan["on"]
                line["off"] = plan["off"]
            result.append(line)
        else:
            if line["line"] != 0:
                result.append(line)
    return Success(result)


