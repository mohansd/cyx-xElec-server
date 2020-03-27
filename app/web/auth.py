# _*_ coding: utf-8 _*_
from flask import redirect, url_for
from . import web

@web.route('/')
def index():
    '''默认跳转的 API 文档'''
    return redirect('/apidocs/#/')

@web.route('/doc')
def doc():
    '''跳转'''
    return redirect(url_for('web.index'))