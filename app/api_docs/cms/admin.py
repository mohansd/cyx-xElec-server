# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2020/3/24.
"""
from app.libs.swagger_filed import StringQueryFiled, StringPathFiled, BodyField
__author__ = 'Allen7D'

# 权限
group_id_in_path = StringPathFiled(
    name='group_id', description="权限组ID", enum=['1', '2', '3', '4', '5', '10', '15', '20'], required=True)
group_id_in_query = StringQueryFiled(
    name='group_id', description="权限组ID", enum=['1', '2', '3', '4', '5', '10', '15', '20'], required=True)