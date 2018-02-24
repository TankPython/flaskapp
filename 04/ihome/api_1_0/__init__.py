#coding:utf-8
from flask import Blueprint

api = Blueprint("api_1_0",__name__)

# 导入蓝图的视图
from . import demo2,verify,passport   #笔记
# from . import verify
# from . import passport
