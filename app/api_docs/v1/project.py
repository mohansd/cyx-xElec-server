# -*- coding: utf-8 -*-


project_list = {
    "parameters": [{
        "name": "project_id",
        "description": "企业项目ID",
        "type": "string",
        "in": "path",
        "required": "true"
    }],
    "response": {
        "200": {
            "description": "获取成功",
            "examples": {
                "data": [
                    {
                        "projectName": "金峰",
                        "projectId": "test",
                        "deviceNum": 2,
                        "online": 1,
                        "alarmNum": 5
                    }
                ],
                "error_code": 0,
            }
        }
    }
}

add_project = {
    "parameters": [{
        "name": "body",
        "in": "body",
        "description": "新增项目组",
        "require": "true",
        "schema": {
            "id": "add_project",
            "required": ["projectName", "device"],
            "properties": {
                "projectName": {
                    "type": "string",
                    "description": "项目名",
                    "enum": ["金峰"],
                    "default": "金峰"
                },
                "device": {
                    "type": "array",
                    "description": "设备列表",
                    "item": {
                        "type": "string",
                        "description": "设备ID",
                        "enum": ["123"],
                        "default": "123"
                    },
                    "enum": [["123", "321"]],
                    "default": ["123", "321"]
                }
            }
        }
    }],
    "responses": {
        "200": {
            "description": "新增成功",
            "examples": {}
        }
    }
}

edit_project = {
    "parameters": [{
        "name": "body",
        "in": "body",
        "description": "编辑项目组",
        "require": "true",
        "schema": {
            "id": "edit_project",
            "required": ["projectName", "device"],
            "properties": {
                "projectName": {
                    "type": "string",
                    "description": "项目名",
                    "enum": ["金峰"],
                    "default": "金峰"
                },
                "projectId": {
                    "type": "string",
                    "description": "项目ID",
                    "enum": ["123"],
                    "default": "123"
                }
            }
        }
    }],
    "responses": {
        "200": {
            "description": "编辑成功",
            "examples": {}
        }
    }
}

delete_project = {
    "parameters": [{
        "name": "body",
        "in": "body",
        "description": "删除项目组",
        "require": "true",
        "schema": {
            "id": "delete_project",
            "required": ["projectId"],
            "properties": {
                "projectId": {
                    "type": "string",
                    "description": "项目ID",
                    "enum": ["123"],
                    "default": "123"
                }
            }
        }
    }],
    "responses": {
        "200": {
            "description": "删除成功",
            "examples": {}
        }
    }
}
