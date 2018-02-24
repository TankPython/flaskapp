#coding:utf-8
from . import api
from flask import current_app
from ihome import db,models

print "222222222222222222222222"

@api.route("/index")
def index():
    current_app.logger.error("error info")   # 笔记
    current_app.logger.warn("warn info")
    current_app.logger.info("info info")
    current_app.logger.debug("debug info")
    return "hahahaha2"