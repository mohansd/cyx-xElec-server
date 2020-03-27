# -*- coding: utf-8 -*-
from apscheduler.triggers.combining import AndTrigger
from flask import current_app
from app.models.job import Job
from app.libs.utils import generate_uuid, test_job
from .device import Device


class APScheduler:
    def add_job(self, job_id, func, args, **kwargs):
        job_def = dict(kwargs)
        job_def['id'] = job_id
        job_def['func'] = func
        job_def['args'] = args
        job_def = self.fix_job_def(job_def)
        current_app.apscheduler.scheduler.add_job(**job_def)
        self.pause_job(job_id=job_id)

    def remove_job(self, job_id, jobstore=None):
        current_app.apscheduler.scheduler.remove_job(job_id, jobstore=jobstore)

    def resume_job(self, job_id, jobstore=None):
        current_app.apscheduler.scheduler.resume_job(job_id, jobstore=jobstore)

    def pause_job(self, job_id, jobstore=None):
        current_app.apscheduler.scheduler.pause_job(job_id, jobstore=jobstore)

    def fix_job_def(self, job_def):
        if job_def.get('trigger') == 'data':
            job_def['run_date'] = job_def.get('run_date') or None
        elif job_def.get('trigger') == 'cron':
            job_def['hour'] = job_def.get('hour', "*")
            job_def['minute'] = job_def.get('minute', "*")
            job_def['week'] = job_def.get('week', "*")
            job_def['day'] = job_def.get('day', "*")
            job_def['month'] = job_def.get('month, "*')
        elif job_def.get('trigger') == 'interval':
            job_def['seconds'] = job_def.get('seconds', "*")
        else:
            if job_def.get("andTri"):
                job_def['trigger'] = AndTrigger([job_def.pop("andTri", None), ])
        Job().save_job(job_def=job_def)
        return job_def

    def init_job(self, on, off, line, plan_id):
        for on_time in on:
            print(on_time)
            uuid = generate_uuid()
            job_id = uuid[0:8]
            hour = int(on_time["hour"])
            minute = int(on_time["minute"])
            self.add_job(job_id=job_id, func=Device.operate_job, args=(line, "ON", plan_id, line.device_id, line.id),
                         trigger="cron", hour=hour, minute=minute)
        for off_time in off:
            uuid = generate_uuid()
            job_id = uuid[0:8]
            hour = int(off_time["hour"])
            minute = int(off_time["minute"])
            self.add_job(job_id=job_id, func=Device.operate_job, args=(line, "OFF", plan_id, line.device_id, line.id),
                         trigger="cron", hour=hour, minute=minute)
