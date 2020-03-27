# -*- coding: utf-8 -*-
from .base import Base
from mongoengine import StringField, DictField, ObjectIdField, IntField, ListField


class Job(Base):
    type = StringField()
    job_id = StringField()
    args = ListField()
    func = StringField()
    time_args = DictField()
    creator = ObjectIdField()
    state = IntField()  # 1：启动 0：暂停
    device_id = StringField()
    operate = StringField()
    line_id = ObjectIdField()
    plan_id = ObjectIdField()
    meta = {
        'collection': 'job',
        'strict': True
    }

    @staticmethod
    def save_job(job_def):
        arg = ["operate", "plan_id", "device_id", "line_id"]
        job = Job()
        time_args = {}
        for key, value in job_def.items():
            if key == "trigger":
                job["type"] = value
            elif key == "args":
                args = []
                for i in value:
                    args.append(i)
                job["args"] = args
            elif key == "func":
                job["func"] = getattr(value, '__name__')
            elif key == "id":
                job["job_id"] = value
            else:
                time_args[key] = value
        job["time_args"] = time_args
        job["state"] = 0
        print(job["args"])
        for index in range(len(job["args"])-1):
            job[arg[index]] = job["args"][index+1]
        job.save()
