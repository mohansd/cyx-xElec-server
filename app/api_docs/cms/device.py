# _*_ coding: utf-8 _*_
from app.libs.swagger_filed import IntegerQueryFiled, IntegerPathFiled, StringPathFiled, StringQueryFiled


file_name_in_path = StringPathFiled(name='file_name', description="文件名", enum=['金峰设备录入信息.excel'], default='金峰设备录入信息.excel')

upload_file = {
	"parameters": [
		{
			"name": "file",
			"in": "formData",
			"type": "file",
			"required": 'false'
		},
	],
	"responses": {
		"200": {
			"description": "上传文件成功",
			"examples": {}
		}
	}
}