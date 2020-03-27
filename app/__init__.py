# -*- coding: utf-8 -*-
import os
import json
import time

from flask import redirect, g, request, _request_ctx_stack
from flask_apscheduler import APScheduler
from flask_redis import FlaskRedis

from .app import Flask
from app.models.base import db
from app.api import create_blueprint_list
from app.libs.redprint import route_meta_infos
from app.web import web

scheduler = APScheduler()
redis_client = FlaskRedis()

app = Flask(__name__)


def create_app():
    load_config(app)
    register_blueprint(app)
    register_plugin(app)

    return app


def load_config(app):
    if os.environ.get('DEV_MODE') == 'local':
        app.config.from_object('app.config.local_setting')
        app.config.from_object('app.config.local_secure')
    else:
        app.config.from_object('app.config.secure')
        app.config.from_object('app.config.setting')


def register_plugin(app):
    apply_cors(app)  # 应用跨域扩展，使项目支持请求跨域
    connect_db(app)  # 连接数据库
    init_auth_group(app) # 初始化权限组
    handle_error(app)  # 统一处理异常
    apply_redis(app)  # 应用redis
    apply_scheduler(app)  # 应用scheduler
    apply_excel(app)  # 应用excel

    # Debug模式(以下为非必选应用，且用户不可见)
    if app.config['DEBUG']:
        apply_request_log(app)  # 请求日志打印功能(请求的性能)
        apply_default_router(app)  # 应用默认路由
        apply_orm_admin(app)  # 应用flask-admin, 可以进行简易的 ORM 管理
        apply_swagger(app)  # 应用flassger, 可以查阅Swagger风格的 API文档


def apply_cors(app):
    from flask_cors import CORS
    cors = CORS()
    cors.init_app(app, resources={"/*": {"origins": "*"}})


def connect_db(app):
    db.init_app(app)


def apply_request_log(app):
    @app.before_request
    def request_cost_time():
        g.request_start_time = time.time()
        g.request_time = lambda: "%.5f" % (time.time() - g.request_start_time)

    @app.after_request
    def log_response(res):
        message = '[%s] -> [%s] from:%s costs:%.3f ms' % (
            request.method,
            request.path,
            request.remote_addr,
            float(g.request_time()) * 1000
        )
        try:
            req_body = request.get_json() if request.get_json() else {}
        except Exception as e:
            req_body = {}
        message += "\n\tdata: {\n\t\tpath: %s, \n\t\tquery: %s, \n\t\tbody: %s\n\t} " % (
            json.dumps(_request_ctx_stack.top.request.view_args, ensure_ascii=False),
            json.dumps(request.args, ensure_ascii=False),
            req_body
        )
        # 设置颜色开始(至多3类参数，以m结束)：\033[显示方式;前景色;背景色m
        print('\033[0;34m')
        if request.method in ('GET', 'POST', 'PUT', 'DELETE'):
            print(message)
        print('\033[0m')  # 终端颜色恢复
        return res


def handle_error(app):
    from werkzeug.exceptions import HTTPException
    from app.libs.error import APIException
    from app.libs.error_code import ServerError

    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, APIException):
            return e
        elif isinstance(e, HTTPException):
            code = e.code
            msg = e.description
            error_code = 1007
            return APIException(code, error_code, msg)
        else:
            if not app.config['DEBUG']:
                raise e
                return ServerError()  # 未知错误(统一为服务端异常)
            else:
                print(e)
                raise e


def apply_redis(app):
    redis_client = FlaskRedis(app)
    redis_client.init_app(app)


def apply_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()


def apply_default_router(app):
    @app.route('/')
    def doc():
        '''跳转到「api文档」'''
        return redirect('/apidocs/#/')


def apply_excel(app):
    import flask_excel as excel
    excel.init_excel(app)


def apply_orm_admin(app):
    from flask_admin import Admin
    from flask_admin.contrib.mongoengine import ModelView as _ModelView

    from app.models.user import User
    from app.models.cdkey import CDKey
    from app.models.company import Company
    from app.models.project import Project
    from app.models.device import Device
    from app.models.line import Line

    class ModelView(_ModelView):
        # column_exclude_list = ['createdAt', 'updatedAt', 'cls']
        page_size = 10
        # can_create = False
        # can_edit = False
        # can_delete = False

    admin = Admin(name='ORM 管理', template_mode='bootstrap3')
    for model in [User, CDKey, Company, Project, Device, Line]:
        admin.add_view(ModelView(model))

    apply_file_admin(admin)
    admin.init_app(app, url='/admin')


def apply_file_admin(admin):
    # Admin添加文件管理系统
    from flask_admin.contrib.fileadmin import FileAdmin
    import os.path as op
    path = op.join(op.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='静态资源'))


def apply_swagger(app):
    from flasgger import Swagger
    # 默认与 config/setting.py 的 SWAGGER 合并
    # 可以将secure.py中的SWAGGER全部写入template
    swagger = Swagger(template={'tags': app.config['SWAGGER_TAGS']})
    swagger.init_app(app)


def register_blueprint(app):
    '''注册蓝图'''
    bp_list = create_blueprint_list(app)
    for url_prefix, bp in bp_list:
        app.register_blueprint(bp, url_prefix=url_prefix)
    app.register_blueprint(web, url_prefix='/web')

    mount_route_meta_to_endpoint(app)
    load_endpint_infos(app)


def load_endpint_infos(app):
    """
    返回权限管理中的所有视图函数的信息，包含它所属module
    :return:
    """
    infos = {}
    index = 0
    for ep, meta in app.config['EP_META'].items():
        index += 1
        endpint_info = {'id': index, 'auth': meta.auth, 'module': meta.module}
        module = infos.get(meta.module, None)
        #  infos是否已经存在该module
        if module:
            module.append(endpint_info)
        else:
            infos[meta.module] = [endpint_info]
        app.config['EP_INFO_LIST'].append(endpint_info)
    app.config['EP_INFOS'] = infos
    return infos


def mount_route_meta_to_endpoint(app):
    '''
    将route_mate挂载到对应的endpoint上
    :param app:
    :return:
    '''
    for endpoint, func in app.view_functions.items():
        info = route_meta_infos.get(func.__name__ + str(func.__hash__()), None)
        if info:
            app.config['EP_META'].setdefault(endpoint, info)


def init_auth_group(app):
    '''
    默认的权限组，必须存在于数据库, 项目启动后自动导入。
    '''
    from app.models.group import Group as GroupModel
    auth_groups = app.config['AUTH_GROUPS']
    for key, value in auth_groups.items():
        group = GroupModel.get(name=value.name)
        if not group:
            group = GroupModel.create(name=value.name, info=value.info)
        value = value._replace(id=str(group.id))
        app.config['AUTH_GROUPS'][key] = value
