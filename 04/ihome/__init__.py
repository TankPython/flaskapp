# coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_map
import redis
from flask_session import Session
from flask_wtf import CSRFProtect

import logging
from logging.handlers import RotatingFileHandler

# 1.数据库工具对象
db = SQLAlchemy()
# 2.redis连接对象
redis_store = None

# 日志连接对象
# 配置日志信息
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)

def Create_app(config_name):
    # 创建flask的应用对象；根据配置模式的名字获取配置参数的类；
    app = Flask(__name__)
    class_name = config_map.get(config_name)
    app.config.from_object(class_name)
    # 使用app初始化db
    db.init_app(app)
    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=class_name.REDIS_HOST, port=class_name.REDIS_PORT)
    # 利用flask-session，将session数据保存到redis中；
    Session(app)
    # 为flask补充csrf防护
    CSRFProtect(app)
    #注册蓝图
    from ihome import api_1_0  #笔记  循环导包的问题
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")

    # 注册自定义的转换器
    from ihome.utils import transverer
    app.url_map.converters["re"] = transverer.RegexConverter

    #注册静态文件的蓝图
    from ihome import web_html
    app.register_blueprint(web_html.html)

    return app

