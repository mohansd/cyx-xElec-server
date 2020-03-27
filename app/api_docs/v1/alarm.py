# -*- coding: utf-8 -*-

get_alarm = {
	"parameters": [{
		"name": "body",
		"in": "body",
		"description": "查询告警",
		"require": "true",
		"schema": {
			"id": "get_alarm",
			"required": ["start", "end"],
			"properties": {
				"start": {
					"type": "number",
					"description": "起始时间",
					"enum": [1573847567123],
					"default": 1573847567123
				},
				"end": {
					"type": "number",
					"description": "结束时间",
					"enum": [1573847567123],
					"default": 1573847567123
				}
			}
		}
	}],
	"responses": {
		"200": {
			"description": "获取成功",
			"examples": {
				"data": [],
				"error_code": 0
			}
		}
	}
}
