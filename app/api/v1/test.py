from app.libs.redprint import RedPrint
from app.libs.error_code import Success
from app.api_docs.v1 import user as api_doc
from app.service.socketservice import *
from flask import current_app
import socket
api = RedPrint(name='test', description='测试', api_doc=api_doc)


@api.route('/socket')
def socket_test():
    socket1 = current_app.extensions["redis"].hget("firstsocket", "socket")
    print(socket)
    print(type(socket))
    socket1.sendall("this is socket".encode())
    # print('\n'.join(['%s:%s' % item for item in current_app.__dict__.items()]))
    # print(client_addr)
    # client_socket[0].sendall(('%s %s %s ' % (time.ctime(), "","456")).encode())
    return "success"