# _*_ coding: utf-8 _*_

from app.libs.enums import ScopeEnum


class Scope:
    allow_api = []
    allow_module = []
    forbidden_api = []
    forbidden_module = []

    def __add__(self, other):
        self.allow_api = list(set(self.allow_api + other.allow_api))
        self.allow_module = list(set(self.allow_module + other.allow_module))
        self.forbidden_api = list(set(self.forbidden_api + other.forbidden_api))
        self.forbidden_module = list(set(self.forbidden_module + other.forbidden_module))

        return self

    @staticmethod
    def match_user_scope(auth, type='en'):
        '''
        :param auth(int): 用户权限(1,2,...)
        :param type(str): en(英文) | cn(中文)
        :return:
        '''
        auth_scope_en = {
            # System 系统(金峰)
            ScopeEnum.SYS_SUPER: 'SysSuperScope',
            ScopeEnum.SYS_ADMIN: 'SysAdminScope',
            # Company 企业
            ScopeEnum.CO_SUPER: 'CoSuperScope',
            ScopeEnum.CO_ADMIN: 'CoAdminScope',
            ScopeEnum.CO_PROJECT: 'CoProjectScope',
            ScopeEnum.CO_OPERATE: 'CoOperateScope',
            ScopeEnum.CO_USER: 'CoUserScope',
            # Agent 代理商
            ScopeEnum.AGENT: 'AgentScope',
            # guest 游客
            ScopeEnum.GUEST: 'GuestScope'
        }
        auth_scope_cn = {
            # System 系统(金峰)
            ScopeEnum.SYS_SUPER: '系统超级管理员',
            ScopeEnum.SYS_ADMIN: '系统管理员',
            # Company 企业
            ScopeEnum.CO_SUPER: '企业超级管理员',
            ScopeEnum.CO_ADMIN: '企业管理员',
            ScopeEnum.CO_PROJECT: '项目负责人',
            ScopeEnum.CO_OPERATE: '运维员工',
            ScopeEnum.CO_USER: '普通员工',
            # Agent 代理商
            ScopeEnum.AGENT: '代理商',
            # guest 游客
            ScopeEnum.GUEST: '游客'
        }
        if type == 'en':
            return auth_scope_en.get(ScopeEnum(auth), 'GuestScope')
        elif type == 'cn':
            return auth_scope_cn.get(ScopeEnum(auth), '普通用户')


class SysSuperScope(Scope):
    allow_api = [] + []
    allow_module = [] + []
    forbidden_api = [] + []
    forbidden_module = [] + []

    def __init__(self):
        self + SysAdminScope()


class SysAdminScope(Scope):
    '''
    1.无法操作/查看「项目/设备」
    2.无法授权/收权「运维管理员」、「普通员工」
    '''
    allow_api = [] + []
    allow_module = ['cms.agent'] + ['cms.device_category']
    forbidden_api = [] + []
    forbidden_module = [] + []

    def __init__(self):
        self + CoSuperScope()


class CoSuperScope(Scope):
    '''
    1.CMS端
        包含一切操作
    2.小程序端
        操作/查看所有「项目/设备」
        CRUD「企业管理员、项目管理员、运维管理员、普通员工」
        授权/收权「项目管理员」其权限范围内的「项目/设备」
    '''
    allow_api = [] + []
    allow_module = [] + []
    forbidden_api = [] + []
    forbidden_module = [] + []

    def __init__(self):
        self + CoAdminScope()


class CoAdminScope(Scope):
    '''
    1.CMS端
        包含一切操作
    2.小程序端
        操作/查看所有「项目/设备」
        CRUD「项目管理员、运维管理员、普通员工」
        授权/收权「项目管理员」其权限范围内的「项目/设备」
    '''
    allow_api = [] + []
    allow_module = [] + []
    forbidden_api = [] + []
    forbidden_module = [] + []

    def __init__(self):
        self + CoProjectScope()


class CoProjectScope(Scope):
    '''
    小程序端
        操作/查看「项目/设备」
        授权/收权「运维管理员」、「普通员工」其权限范围内的「项目/设备」
    '''
    allow_api = [] + []
    allow_module = [] + []
    forbidden_api = [] + []
    forbidden_module = [] + []

    def __init__(self):
        self + CoOperateScope()


class CoOperateScope(Scope):
    '''
    小程序端
        操作/查看其权限范围内的「项目/设备」
    '''
    allow_api = [] + []
    allow_module = [] + []
    forbidden_api = [] + []
    forbidden_module = [] + []

    def __init__(self):
        self + CoUserScope()


class CoUserScope(Scope):
    '''
    小程序端
        查看其权限范围内的「项目/设备」
    '''
    allow_api = [] + []
    allow_module = ['v1.user', 'v1.cdkey'] + \
                   ['cms.user', 'cms.cdkey', 'cms.company', 'cms.project', 'cms.device']
    forbidden_api = [] + []
    forbidden_module = [] + []

    def __init__(self):
        pass


class AgentScope(Scope):
    '''
    1.无法操作/查看「项目/设备」
    2.无法授权/收权「运维管理员」、「普通员工」
    3. 生成激活码；查看入驻企业、激活码列表
    4. 修改下线企业的信息（涉及到权限）
    '''
    allow_api = [] + []
    allow_module = [] + []
    forbidden_api = [] + []
    forbidden_module = [] + []

    def __init__(self):
        pass


class GuestScope(Scope):
    '''游客'''
    allow_api = [] + []
    allow_module = [] + []
    forbidden_api = [] + []
    forbidden_module = [] + []

    def __init__(self):
        pass


def is_in_scope(scope, endpoint):
    """
    判断「访问的用户」是否有该接口的权限
    :param scope: number 权限值
    :param endpoint: string 'v1.user+get_user'
    :return: boolean
    """
    scope = globals()[scope]()  # 基于「string类型变量」查找到同名的类
    red_name = endpoint.split('+')[0]  # v1.*: v1.user 或者 cms.user
    blue_name = red_name.split('.')[0]  # v1或者cms
    if red_name in scope.forbidden_module:
        return False
    if endpoint in scope.forbidden_api:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
