#coding:utf-8

from . import api
from flask import request,jsonify,current_app,session
from ..utils.response_code import RET
import re
from ihome import redis_store
from ..models import User
from ihome import db
from sqlalchemy.exc import IntegrityError

@api.route("/users",methods=["POST"])
def register():
    #1.请求的参数： 手机号、短信验证码、密码、确认密码
    json_dict = request.get_json()
    mobile = json_dict.get("mobile")
    phone_code = json_dict.get("phoneCode")
    passwd = json_dict.get("passwd")
    passwd2 = json_dict.get("passwd2")

    #校验参数
    if not all([mobile,phone_code,passwd,passwd2]):
        return jsonify(errno=RET.DATAERR,errmsg="参数不完整")
    #判断手机号格式
    ret = re.match(r"1[35689]\d{9}",mobile)
    if ret is None:
        return jsonify(errno=RET.DATAERR,errmsg="手机号格式错误")
    #从redis中取出短信验证码，判断短信验证码是否过期
    try:
        sms_code= redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="验证码数据库操作错误")
    if sms_code is None:
        return jsonify(errno=RET.DATAERR,errmsg="短信验证码过期，请重新验证")
    #删除redis中的短信验证码，防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    #判断用户填写短信验证码的正确性
    if phone_code != sms_code:
        return jsonify(errno=RET.DATAERR,errmsg="短信验证码填写错误，请重新验证")
    #保存用户的注册数据到数据库中
    user = User(name=mobile,mobile=mobile)
    user.password = passwd
    # print user.password
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DATAERR, errmsg="数据库重复")
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DATAERR,errmsg="数据库保存错误")

    # 保存登录状态到session中
    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id
    #返回结果
    return jsonify(errno=RET.OK, errmsg="ok no problem")


