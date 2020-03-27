# -*- coding: utf-8 -*-
from app.libs.swagger_filed import IntegerQueryFiled

state_in_query = IntegerQueryFiled(name='state', description="激活码状态(0: 失效; 1:激活)", enum=[0, 1], default=0)
