# -*- coding: utf-8 -*-
import datetime
from .utils import zero_time, last_month_datetime, month_datetime
from app.models.monitor import Monitor
from app.models.line import Line
from app.models.statistics_hour import StatisticsHour
from app.models.statistics import Statistics
from app.models.statistics_energy_avg import EnergyAvg
from bson.objectid import ObjectId


def per_hour_statistics():
    now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    last_hour = now - datetime.timedelta(minutes=60)
    last_two_hour = now - datetime.timedelta(minutes=120)
    lines = Line.objects.all()
    for line in lines:
        max_energy_monitor = Monitor.objects.filter(line_id=line.id, type="energy", createdAt__gte=last_hour,
                                                    createdAt__lt=now).order_by("-createdAt").first()
        min_energy_monitor = Monitor.objects.filter(line_id=line.id, type="energy", createdAt__gte=last_two_hour,
                                                    createdAt__lt=last_hour).order_by("-createdAt").first()
        if max_energy_monitor and min_energy_monitor:
            max_energy = max_energy_monitor["value"]
            min_energy = min_energy_monitor["value"]
            energy = max_energy - min_energy
        elif max_energy_monitor and min_energy_monitor is None:
            max_energy = max_energy_monitor["value"]
            min_energy = Monitor.objects.filter(line_id=line.id, type="energy", createdAt__gte=last_hour,
                                                createdAt__lt=now).order_by("+createdAt").first()["value"]
            energy = max_energy - min_energy
        else:
            energy = 0

        StatisticsHour.create(zero_time=zero_time(), device_id=line.device_id, line_id=line.id, hour_time=last_hour,
                              energy=energy)


def per_day_statistics():
    today = zero_time()
    yesterday = zero_time() - datetime.timedelta(days=1)
    before_yesterday = yesterday - datetime.timedelta(days=1)
    lines = Line.objects.all()
    for line in lines:
        max_energy_monitor = Monitor.objects.filter(line_id=line.id, type="energy", createdAt__gte=yesterday,
                                                    createdAt__lt=today).order_by("-createdAt").first()
        min_energy_monitor = Monitor.objects.filter(line_id=line.id, type="energy", createdAt__gte=before_yesterday,
                                                    createdAt__lt=yesterday).order_by("-createdAt").first()
        if max_energy_monitor and min_energy_monitor:
            max_energy = max_energy_monitor["value"]
            min_energy = min_energy_monitor["value"]
            energy = max_energy - min_energy
        elif max_energy_monitor and min_energy_monitor == []:
            max_energy = max_energy_monitor["value"]
            min_energy = Monitor.objects.filter(line_id=line.id, type="energy", createdAt__gte=yesterday,
                                                createdAt__le=today).order_by("+createdAt").first()
            energy = max_energy - min_energy
        else:
            energy = 0
        Statistics.create(zero_point=yesterday, date_type="day", data_type="energy", device_id=line.device_id,
                          line_id=line.id, value=energy)


def energy_avg_statistics():
    last_month = last_month_datetime()
    this_month = month_datetime()
    lines = Line.objects.all()
    for line in lines:
        match = {"$match": {"line_id": line.id, "hour_time": {"$gte": last_month, "$lt": this_month}}}
        group = {"$group": {"_id": {"$hour": "$hour_time"}, "energy": {"$avg": "$energy"}}}
        sort = {"$sort": {"_id": 1}}
        result = StatisticsHour.objects.aggregate(*[match, group, sort])
        for r in result:
            EnergyAvg.create(month_time=last_month, hour=r["_id"], device_id=line.id, line_id=line.id,
                             energy=r["energy"])
