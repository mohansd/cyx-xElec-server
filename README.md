# xElec-server

<h4 align="center">
	金峰项目(xElec)服务端
</h4>

## 本地&线上同步推进
### 业务场景
本地与线上的 Swagger API 文档的接口的地址是不同的，但都依赖同一个配置文件 **`app\config\setting.py`**。<br>
而个人项目有着本地和线上同步，开发和测试同步的需求，会不断修改 **`app\config\setting.py`** 文件，无法用 **`.gitignore`** 做到忽略配置文件，本地和线上配置隔离的效果。 

### 解决
**`本地`** 和 **`线上`** 自动根据所处的环境(由 .gitignore 控制)不同，选择不同的配置文件。<br>
那么， **`本地`** 可以比 **`线上`** 多了 **`app/config/dev.py`** 文件; 基于该文件的存在与否，可以用 **`if else`** 控制 **`app/config/`** 中配置输出。

### 实践
1. `echo "/app/config/dev.py" >> .gitignore` # 追加 Git 忽略提交配置到 .gitignore
2. 新建 **`app/config/dev.py`** 文件

### 本地启动
```
$ git clone http://gitlab.51anquan.org/xElec/xElec-server.git
$ cd xElec-server
$ touch app/config/dev.py # 如果是在服务器上，则忽略执行此命令
$ mkdir .venv # 生成.venv文件夹，用于存放该项目的python解释器(包括后续所有安装的包依赖)
$ pipenv --python 3.6 # 指定某 Python 版本创建环境
$ pipenv shell # 激活虚拟环境 or 如果没有虚拟环境，则构建新的(默认版本)
$ pipenv install # 安装包依赖
$ python server.py run # 启动方式1:默认5000端口
$ python server.py run -p 8020 # 启动方式2:改为8020端口
$ python server.py run -h 0.0.0.0 -p 8020 # 启动方式3:以本地IP地址访问
```

### 查阅 API文档(本项目)
> 启动服务(DEBUG 模式下)<br>
在浏览器端输入：http://localhost:8020/apidocs/#/


## 服务器部署
本项目选择在 Ubuntu 16.04 上，用 Nginx + Gunicorn + Pipenv 部署，其中 Gunicorn 取代 uWsgi。
> Flask 与 uWsgi 结合有许多难以处理的 bug