#coding:utf-8
from . import api
from ..utils.captcha.captcha import captcha
from ihome import redis_store
from ihome import constants
from flask import current_app,jsonify,make_response
from ..utils.response_code import RET

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
        return jsonify(errorno=RET.DATAERR,errormsg="保存图片数据失败")  #笔记1.30
    resp = make_response(img)
    resp.headers["Content-Type"] = "image/jpg"  #笔记 1.30 不设定的时候会返回二进制数据  因为默认类型是text/html，不过也能返回图片
    return resp
