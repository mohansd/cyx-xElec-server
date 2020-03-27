# _*_ coding: utf-8 _*_
"""
  设备类型(按照规格化分)
"""
from app.libs.swagger_filed import IntegerQueryFiled, IntegerPathFiled, StringPathFiled, StringQueryFiled

category_id_in_path = StringPathFiled(name='category_id', description="类别(规格)ID",
                                      enum=['5e744ca1c1409608f36178dc',
                                            '5e744d3d988c4a71f162886a'],
                                      default='5e744ca1c1409608f36178dc',
                                      required=True)
