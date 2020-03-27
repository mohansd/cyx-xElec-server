# -*- coding: utf-8 -*-

from werkzeug.middleware.proxy_fix import ProxyFix
from flask_script import Manager, Server

from app import create_app
from app.service import socketservice

app = create_app()

app.wsgi_app = ProxyFix(app.wsgi_app)
manager = Manager(app)
manager.add_command("run", Server(use_debugger=False))

if __name__ == '__main__':
	socketservice.get_instance()
	# manager.run() # 终端运行 python server.py run -h 0.0.0.0 -p 8020 效果如下
	app.run(host="0.0.0.0", port=8020, debug=False)
