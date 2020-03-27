# -*- coding: utf-8 -*-

unused_device_list = {
    "parameters": [{
        "name": "company_id",
        "description": "企业ID",
        "type": "string",
        "in": "path",
        "required": True
    }],
    "response": {
        "200": {
            "description": "获取成功",
            "examples": {
                "data": [
                    {
                        "deviceId": "test",
                        "cloudId": "test",
                        "alias": "test"
                    }
                ],
                "error_code": 0,
            }
        }
    }
}

used_device_list = {
    "parameters": [{
        "name": "company_id",
        "description": "企业ID",
        "type": "string",
        "in": "path",
        "required": True
    }],
    "response": {
        "200": {
            "description": "获取成功",
            "examples": {
                "data": [
                    {
                        "deviceId": "test",
                        "cloudId": "test",
                        "alias": "test",
                        "projectName": "test"
                    }
                ],
                "error_code": 0,
            }
        }
    }
}

device_list = {
    "parameters": [{
        "name": "project_id",
        "description": "项目ID",
        "type": "string",
        "in": "path",
        "required": True
    }],
    "response": {
        "200": {
            "description": "获取成功",
            "examples": {
                "data": [
                    {
                        "deviceId": "test",
                        "cloudId": "test",
                        "alias": "test",
                        "energy": "test",
                        "status": "test",
                        "electric": "test",
                        "alarmNum": 3
                    }
                ],
                "error_code": 0,
            }
        }
    }
}

edit_device = {
    "parameters": [{
        "name": "body",
        "in": "body",
        "description": "编辑设备",
        "require": "true",
        "schema": {
            "id": "edit_device",
            "required": ["deviceId", "alias", "location", "electricity"],
            "properties": {
                "deviceId": {
                    "type": "string",
                    "description": "设备ID",
                    "enum": ["123"],
                    "default": "123"
                },
                "alias": {
                    "type": "string",
                    "description": "别名",
                    "enum": ["1号"],
                    "default": "1号"
                },
                "location": {
                    "type": "object",
                    "description": "设备位置",
                    "item": {
                        "type": "object",
                        "properties": {
                            "sheng": {
                                "type": "string",
                                "description": "省份",
                                "enum": ["浙江省"],
                                "default": "浙江省"
                            },
                            "shi": {
                                "type": "string",
                                "description": "市",
                                "enum": ["杭州市"],
                                "default": "杭州市"
                            },
                            "qu": {
                                "type": "string",
                                "description": "区",
                                "enum": ["萧山区"],
                                "default": "萧山区"
                            }
                        }
                    },
                    "enum": [{
                        "sheng": "浙江省",
                        "shi": "杭州市",
                        "qu": "萧山区"
                    }],
                    "default": {
                        "sheng": "浙江省",
                        "shi": "杭州市",
                        "qu": "萧山区"
                    }
                },
                "electricity": {
                    "type": "number",
                    "description": "电流阈值",
                    "enum": [1.5],
                    "default": 1.5
                }
            }
        }
    }],
    "response": {
        "200": {
            "description": "编辑成功",
            "examples": {}
        }
    }
}

operate_device = {
    "parameters": [{
        "name": "body",
        "in": "body",
        "description": "操作设备",
        "required": "true",
        "schema": {
            "id": "operate_device",
            "required": ["deviceId", "lineId", "type"],
            "properties": {
                "deviceId": {
                    "type": "string",
                    "description": "设备ID",
                    "enum": ["123"],
                    "default": "123"
                },
                "lineId": {
                    "type": "string",
                    "description": "线路ID",
                    "enum": ["123"],
                    "default": "123"
                },
                "type": {
                    "type": "integer",
                    "description": "操作类型",
                    "enum": [1],
                    "default": 1
                }
            }
        }
    }],
    "response": {
        "200": {
            "description": "操作成功",
            "examples": {}
        }
    }
}

# 无法确定有哪些状态
device_status = {
    "parameters": [{
        "name": "device_id",
        "in": "path",
        "description": "设备ID",
        "type": "string",
        "required": "true",
    }],
    "response": {
        "200": {
            "description": "获取成功",
            "examples": {}
        }
    }
}

device_detail = {
    "parameters": [{
        "name": "device_id",
        "in": "path",
        "description": "设备ID",
        "type": "string",
        "required": "true",
    }],
    "response": {
        "200": {
            "description": "获取成功",
            "examples": {
                "data": {
                    "alias": "",
                    "job": []
                }
            }
        }
    }
}
