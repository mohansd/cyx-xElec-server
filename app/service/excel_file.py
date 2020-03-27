# _*_ coding: utf-8 _*_
"""
  Excel文件相关处理
  参考 https://github.com/xcbdjazk/excel_flask/blob/master/app.py
"""
import re
import xlrd
from xlrd import xldate_as_tuple
from datetime import datetime

from app.libs.error_code import ExcelHeadException
from app.libs.enums import ExcelTypeEnum
from app.models.device import Device as DeviceModel
from app.models.device_category import DeviceCategory as DeviceCategoryModel


class ExcelService():
    def __init__(self, file):
        self.file = file
        self.head_fields_cn = [
            '配电柜ID', '采集器云ID', '产品规格', '物联网卡ICCID', '出厂日期', '合同编号',
            # '代理商名称', '代理商联系人', '代理商联系方式', '使用单位名称', '使用单位联系人', '使用单位联系方式'
        ]
        self.head_fields_en = [
            'device_id', 'cloud_id', 'category_name', 'icc_id', 'delivery_time', 'contract_no',
            # 'agent_name', 'agent_user', 'agent_mobile', 'company_name', 'company_user', 'company_mobile'
        ]

    @property
    def origin_excel(self):
        return xlrd.open_workbook(file_contents=self.file.read())

    def load_data(self):
        sheet = self.origin_excel.sheets()[0]
        upload_excel_head_fields = sheet.row_values(0)
        self.__check_excel_head_fields(upload_excel_head_fields)
        title_dict = {item: list(upload_excel_head_fields).index(item) for item in self.head_fields_cn}

        row_list = self.__load_data_by_row(sheet)  # 按行读取，生成二级数据[[],[]]
        row_list = self.__place_data_by_regular(row_list, title_dict)  # 将每一行的数据放置到正确的位置，生成[{}, {}]
        row_list = self.__filter_data(row_list)  # 去掉不符合规范的数据

        device_list = DeviceModel.objects.insert([DeviceModel(**item) for item in row_list])
        return device_list
        # return {
        #     'total': len(device_list)
        # }

    def __check_excel_head_fields(self, upload_excel_head_fields):
        '''
        检查「上传的Excel文件」的表头字段是否合格，其中self.head_fields_cn为标准字段集
        :param upload_excel_head_fields: 上传Excel文件的表头字段
        :return:
        '''
        lost_fields = []
        for field in set(self.head_fields_cn):
            if field not in set(upload_excel_head_fields):
                lost_fields.append(field)

        if len(lost_fields) != 0:
            raise ExcelHeadException(msg='表头字段缺失: {}'.format(lost_fields))

    def __load_data_by_row(self, sheet):
        row_list = []
        nrows, ncols = sheet.nrows, sheet.ncols
        for i_row in range(1, nrows):
            row_data_list = []
            for i_col in range(ncols):
                data = sheet.cell_value(i_row, i_col)  # 定位到的数据
                data_ctype = sheet.cell(i_row, i_col).ctype  # 数据类型
                if ExcelTypeEnum(data_ctype) == ExcelTypeEnum.DATE:
                    data = datetime(*xldate_as_tuple(data, 0))
                row_data_list.append(data)
            row_list.append(row_data_list)
        return row_list

    def __place_data_by_regular(self, prev_row_list, regular_dict):
        '''
        :param prev_row_list: [[],[]]
        :param regular_dict: 排序的规则
        :return:
        '''
        category_list = DeviceCategoryModel.objects.filter().all_or_404()
        category_dict = {
            category.name: category.id for category in category_list
        }
        next_row_list = []
        for row in prev_row_list:
            exchange_row_data_list = []
            for item, index in regular_dict.items():
                data = row[index]  # 定位到的数据
                exchange_row_data_list.append(data)

            row_data_dict = {}
            for j in range(len(self.head_fields_en)):
                row_data_dict[self.head_fields_en[j]] = exchange_row_data_list[j]
            row_data_dict['category_id'] = category_dict.get(row_data_dict['category_name'], '默认规格')
            row_data_dict.pop('category_name')
            next_row_list.append(row_data_dict)
        return next_row_list

    def __filter_data(self, prev_row_list):
        '''过滤数据'''
        next_row_list = []  # 录入的数据
        for row in prev_row_list:
            if row['device_id'] and _has_pure_alnum(row['device_id']):
                next_row_list.append(row)
        return next_row_list


def _has_hanzi(raw):
    rule = re.compile(u'[\u4e00-\u9fa5]')
    return True if rule.search(raw) else False


def _has_pure_alnum(raw):
    return raw.isalnum() and not _has_hanzi(raw)
