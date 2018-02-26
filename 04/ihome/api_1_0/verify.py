#coding:utf-8
from . import api
from ..utils.captcha.captcha import captcha
from ihome import redis_store,constants
from flask import current_app,jsonify,make_response,request
from ..utils.response_code import RET
from ihome.models import User
from ihome.libs.yuntongxun.sms import ccp
import random
from ihome.tasks.sms.tasks import send_sms

# 1.视图处理请求，接收前端的验证码的编号
@api.route("/img_codes/<code_id>")
def verify_code(code_id):
    #2.调用第三方包获取 名字，真实文本， 图片数据；
    name,text,img = captcha.generate_captcha()
    try:
        #3.redis存储名字，过期时间，记录值（异常处理）
        redis_store.setex("img_code_id%s"%code_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)  #笔记1.30
    except Exception as e:
        #4.如果异常就记录日志，返回异常信息
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="保存图片数据失败")  #笔记1.30
    resp = make_response(img)
    resp.headers["Content-Type"] = "image/jpg"  #笔记 1.30 不设定的时候会返回二进制数据  因为默认类型是text/html，不过也能返回图片
    return resp

@api.route("/sms_codes/<re(r'1[34589]\d{9}'):mobile>")
def smscode(mobile):
    #获取图片验证码的值和图片的id
    img_code = request.args.get("code")
    code_id = request.args.get("codeId")

    #校验图片验证码；参数完整性
    if not all([img_code,code_id]):
        return jsonify(errno=RET.DATAERR,errmsg="图片验证码参数不完整")

    #从redis中取出真实的图片验证码
    try:
        real_img_code = redis_store.get("img_code_id%s"%code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="redis连接错误")

    # 判断图片验证码是否过期
    if real_img_code is None:
        return jsonify(errno=RET.DATAERR,errmsg="图片验证码已经过期，请重新验证")

    #删除redis中的图片验证码，防止用户使用同一个图片验证码验证多次
    try:
        redis_store.delete("img_code_id%s"%code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="图片验证码删除错误")

    #与用户填写的图片验证码的值进行对比，错误就返回结果
    if real_img_code.lower() != img_code.lower():
        return jsonify(errno=RET.DATAERR,errmsg="图片验证码填写错误")

    #判断手机号是否存在，如果手机号不存在，则生成短信验证码
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user:
            return jsonify(errno=RET.DATAERR, errmsg="手机号已经存在")
    # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        checkcode = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        # return jsonify(errno=RET.DATAERR, errmsg="redis连接错误验证码校验")
    else:
        if checkcode:
            return jsonify(errno=RET.DATAERR, errmsg="您的操作太频繁60秒后再尝试")
    # 生成验证码
    code = "%06d" % random.randint(0, 1000000)

    # 保存真实的短信验证码
    try:
        redis_store.setex("sms_code_%s" % mobile, 120, code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")

    # 发送短信
    # try:
    rets = send_sms.delay(mobile, [code, "5"], 1)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DATAERR, errmsg="发送异常")
    ret = rets.get()
    print "4444444444444444444484885%s"%ret
    # if ret == "0":
    #     return jsonify(errno=RET.OK, errmsg="发送成功")
    # else:
    return jsonify(errno=RET.OK, errmsg="发送失败11111")

"""1.获取短信验证码
     /保存发送给这个手机号的记录，防止用户在60s内再次发出发送短信的操作/
      """