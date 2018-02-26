# coding:utf-8
from ihome.tasks.main import celery_app
from ihome.libs.yuntongxun.sms import ccp

@celery_app.task
def send_sms(to,time,num):
    try:
        result = ccp.send_template_sms(to, time, num)
    except Exception as e:
        result = -2
    return result
