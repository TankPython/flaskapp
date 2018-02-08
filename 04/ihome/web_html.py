#coding:utf-8

from flask import Blueprint,current_app,make_response
from flask_wtf import csrf

#创建静态文件的蓝图
html = Blueprint("html",__name__)

@html.route("/<re(r'.*'):html_file_name>")
def web_html(html_file_name):
    #1.如果html_file_name为"", 表示访问的路径是/ ,请求的是主页
    if html_file_name =="":
        html_file_name = "index.html"

    #2.如果资源名不是favicon.ico
    if html_file_name != "favicon.ico":
        html_file_name = "html/"+ html_file_name

    #3.创建一个csrf_token值
    csrt_token = csrf.generate_csrf()
    #4.flask提供的返回静态文件的方法
    resp = make_response(current_app.send_static_file(html_file_name))
    # 5.设置cookie值
    resp.set_cookie("csrf_token",csrt_token)
    return resp

