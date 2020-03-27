# -*- coding: utf-8 -*-
from .socketservice import get_instance
from .alarm_service import AlarmService
import binascii
import time
from app.models.device import Device as DeviceModel
from app.models.line import Line
from app.models.monitor import Monitor
from datetime import datetime
from app.libs.utils import dynamic_decimal
from app.libs import command
from app.libs.utils import command_encode
from app.libs.error_code import DeviceException


class Device:
    energy_sign = ["0B04", "0C04", "0D04", "OE04"]
    energy_line = {
        "0B04": 0,
        "0C04": 1,
        "0D04": 2,
        "0E04": 3
    }
    upload_sign = ["CD11", "CD12", "CD21", "CD22", "CD31", "CD32", "CD41", "CD42"]
    upload_type = {
        "1": "ua",
        "2": "energy"
    }
    upload_line = {
        "1": 0,
        "2": 1,
        "3": 2,
        "4": 3
    }
    di = {
        "1": "off",
        "0": "on"
    }
    do = {
        "1": "on",
        "0": "off"
    }

    def __init__(self):
        self.device_id = None
        self.cloud_id = None
        self.version = None
        self.sign = None

    def parse_data(self, data, socket):
        print(datetime.now().strftime('%H:%M:%S'), data)
        if str.startswith(data, "AA55"):
            self.parse_device_data(data, socket)
        elif not self.check_register(socket):
            Device.get_basic_info(socket)
        elif str.startswith(data, "6403") or str.startswith(data, "DD016403"):
            self.parse_modbus_data(data, socket)
        elif self.check_energy_data(data):
            self.parse_energy_data(data, socket)
        elif self.check_upload_data(data):
            self.parse_upload_data(data, socket)
        else:
            print("其他数据", data)

    @staticmethod
    def get_basic_info(socket):
        """获取基础信息，初始化"""
        print("获取cloud_id")
        socket.request.sendall(binascii.a2b_hex("AA550006E00000910177"))
        time.sleep(0.5)
        print("获取信号强度")
        socket.request.sendall(binascii.a2b_hex("AA550004E0230107"))
        time.sleep(0.5)
        print("获取线路状态")
        socket.request.sendall(binascii.a2b_hex("6403001000084C3C"))

    @staticmethod
    def get_cloud_id(socket):
        """获取云ID"""
        socket.request.sendall(command_encode(command.BASIC["cloud_id"]))

    @staticmethod
    def get_version(socket):
        """获取版本"""
        socket.request.sendall(command_encode(command.BASIC["version"]))

    @staticmethod
    def get_sign_strength(socket):
        """获取信号强度"""
        socket.request.sendall(command_encode(command.BASIC["sign"]))

    @staticmethod
    def operate(line, operate, socket):
        """操作电路通断"""
        operate = operate.upper()
        if line in getattr(command, operate).keys():
            socket.request.sendall(command_encode(getattr(command, operate)[line]))

    @staticmethod
    def get_box_detail(socket):
        for e in command.ENERGY.values():
            socket.request.sendall(command_encode(e))
            time.sleep(0.5)
        for u in command.UA.values():
            socket.request.sendall(command_encode(u))
            time.sleep(0.5)

    @staticmethod
    def send_command(socket, command):
        socket.request.sendall(command_encode(command))

    def parse_device_data(self, data, socket):
        if not self.check_devicec_data(data):
            return
        if str.startswith(data, "aa550010e000000a0091".upper()):
            cloud_id = self.parse_cloud_id(data)
            self.register(cloud_id, socket)
        if "EE01" in data:
            version = self.parse_version(data)
            self.version = version
            print("version", version)
        if "E023" in data:
            sign = self.parse_sign(data)
            socket.sign = sign
            self.sign = sign
            print("sign", sign)

    def parse_modbus_data(self, data, socket):
        if str.startswith(data, "DD01"):
            data = data[4:]
        if not self.check_modbus_data(data):
            return
        data = data[6:-4]
        status_map = {
            1: data[3:4],
            2: data[7:8],
            3: data[11:12],
            4: data[15:18]
        }
        do_map = {
            1: data[19:20],
            2: data[23:24],
            3: data[27:28],
            4: data[31:32]
        }
        lines = Line.objects.filter(device_id=socket.device_id).all()
        for line in lines:
            if line.line in status_map.keys():
                status = self.di[status_map[line.line]]
                do = self.do[do_map[line.line]]
                value = {
                    "device_id": socket.device_id,
                    "line_id": line.id,
                    "line": line.line,
                    "type": "status",
                    "value": {
                        "status": status,
                        "do": do
                    }
                }
                Device.switch_alarm(line, status)
                Monitor.save_data(value)

    def parse_cloud_id(self, data):
        cloud_id = data[20:-4]
        return cloud_id

    def parse_version(self, data):
        sign_index = data.index("EE01")
        version = data[sign_index + 4:-4]
        return version

    def parse_sign(self, data):
        sign_index = data.index("E023")
        sign = data[sign_index + 4:-4]
        return int(sign, 16)

    def parse_line_status(self, data):
        pass

    def parse_energy_data(self, data, socket):
        sign = data[0:4]
        line = Line.objects.filter(line=self.energy_line[sign], device_id=socket.device_id).first()
        value = {
            "device_id": socket.device_id,
            "line": line.line,
            "line_id": line.id
        }
        if len(data) < 20:
            data = data[6:-4]
            energy = int(data, 16) // 100
            value["type"] = "energy"
            value["value"] = energy
        else:
            data = data[6:-4]
            voltage_a = int(data[0:4], 16) // 10
            voltage_b = int(data[4:8], 16) // 10
            voltage_c = int(data[8:12], 16) // 10
            value["type"] = "voltage"
            value["value"] = {
                "a": voltage_a,
                "b": voltage_b,
                "c": voltage_c
            }
            Monitor.save_data(value)
            electricity_a = dynamic_decimal((int(data[12:16], 16) / 100))
            electricity_b = dynamic_decimal((int(data[16:20], 16) / 100))
            electricity_c = dynamic_decimal((int(data[20:24], 16) / 100))
            value["type"] = "electricity"
            value["value"] = {
                "a": electricity_a,
                "b": electricity_b,
                "c": electricity_c
            }
            Monitor.save_data(value)
        print("这是解析电能数据", socket.line_status)

    def parse_upload_data(self, data, socket):
        print("开始解析upload")
        print(socket.device_id)
        line = Line.objects.filter(line=self.upload_line[data[2]], device_id=socket.device_id).first()
        type = self.upload_type[data[3]]
        value = {
            "device_id": socket.device_id,
            "line": line.line,
            "line_id": line.id
        }
        if type == "energy":
            energy = (int(data[10:18], 16) // 100)
            value["type"] = "energy"
            value["value"] = energy
            Monitor.save_data(value)
        if type == "ua":
            electricity_a = dynamic_decimal((int(data[22:26], 16)) / 100)
            electricity_b = dynamic_decimal((int(data[26:30], 16)) / 100)
            electricity_c = dynamic_decimal((int(data[30:34], 16)) / 100)
            value["type"] = "electricity"
            value["value"] = {
                "a": electricity_a,
                "b": electricity_b,
                "c": electricity_c
            }
            Monitor.save_data(value)
            voltage_a = int(data[10:14], 16) // 10
            voltage_b = int(data[14:18], 16) // 10
            voltage_c = int(data[18:22], 16) // 10
            value["type"] = "voltage"
            value["value"] = {
                "a": voltage_a,
                "b": voltage_b,
                "c": voltage_c
            }
            Monitor.save_data(value)
            Device.current_alarm(line, electricity_a, electricity_b, electricity_c)
        socket.timestamp = int(round(time.time() * 1000))

    @staticmethod
    def status(socket):
        """获取线路状态"""
        print("获取线路状态")
        socket.request.sendall(command_encode(command.BASIC["line_status"]))

    def check_devicec_data(self, data):
        if len(data) < 8:
            return False
        length = int(data[4:8], 16) * 2
        if len(data[8:]) == length:
            return True
        else:
            return False

    def check_modbus_data(self, data):
        length = int(data[4:6], 16) * 2
        print("length", length)
        print("data", len(data[6:-4]))
        if len(data[6:-4]) == length:
            return True
        else:
            return False

    def check_upload_data(self, data):
        if data[0:4] in self.upload_sign:
            return True
        else:
            return False

    def check_register(self, socket):
        if socket.cloud_id is None:
            return False
        else:
            return True

    def check_energy_data(self, data):
        if data[0:4] in self.energy_sign:
            if self.check_modbus_data(data):
                return True
            else:
                return False
        else:
            return False

    def register(self, cloud_id, socket):
        socket.cloud_id = cloud_id
        self.cloud_id = cloud_id
        device = DeviceModel.objects.filter(cloud_id=cloud_id).first()
        if device:
            socket.device_id = device["device_id"]
            get_instance().add_client(cloud_id, socket)

    @staticmethod
    def update_device(socket):
        for i in range(0, 3):
            Device.status(socket)
            time.sleep(0.5)

    @staticmethod
    def search_device_socket(device_id):
        device = DeviceModel.objects.filter(device_id=device_id).first_or_404()
        cloud_id = device["cloud_id"]
        clients = get_instance().clients
        if cloud_id in clients.keys():
            return clients[cloud_id]
        else:
            raise DeviceException()

    @staticmethod
    def operate_device_plan(device_id, line_id, operate):
        device = DeviceModel.objects.filter(device_id=device_id).first()
        if device:
            cloud_id = device["cloud_id"]
            clients = get_instance().clients
            if cloud_id in clients:
                line = Line.objects.filter(id=line_id).first()
                socket = clients[cloud_id]
                socket.request.sendall(command_encode(getattr(command, operate)[line.line]))

    @staticmethod
    def current_alarm(line, la, lb, lc):
        limit = line.limit
        total = la + lb + lc
        if (limit * (line.standard / 100)) < total < (limit * 1.1):
            alarm = AlarmService(device_id=line.device_id, alarm_type="high_current", line_id=line.id, a=la, b=lb, c=lc,
                                 limit=line.limit)
            alarm.gen_alarm()
        if total > (limit * 1.1):
            alarm = AlarmService(device_id=line.device_id, alarm_type="overload", line_id=line.id, a=la, b=lb, c=lc)
            alarm.gen_alarm()

    @staticmethod
    def offline_alarm(socket):
        device_id = socket.device_id
        alarm = AlarmService(device_id=device_id, alarm_type="offline", line_id=None)
        alarm.gen_alarm()

    @staticmethod
    def trip_alarm(line):
        alarm = AlarmService(device_id=line.device_id, alarm_type="trip", line_id=line.id)
        alarm.gen_alarm()

    @staticmethod
    def switch_alarm(line, status):
        monitor = Monitor.objects.filter(device_id=line.device_id, line_id=line.id, type="status").first()
        if monitor:
            if monitor["value"]["status"] != status:
                if status == "on":
                    alarm = AlarmService(device_id=line.device_id, alarm_type="switch", line_id=line.id, type="on")
                    alarm.gen_alarm()
                else:
                    alarm = AlarmService(device_id=line.device_id, alarm_type="switch", line_id=line.id, type="off")
                    alarm.gen_alarm()

    @staticmethod
    def operate_job(line, operate, *args):
        device_id = line.device_id
        device = DeviceModel.objects.filter(device_id=device_id).first()
        cloud_id = device.cloud_id
        clients = get_instance().clients
        if cloud_id in clients.keys():
            socket = clients[cloud_id]
            for i in range(0, 3):
                Device.operate(line.line, operate, socket)
                time.sleep(0.5)
