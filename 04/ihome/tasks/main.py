# coding:utf-8
from celery import Celery
from ihome.tasks import config
#定义celery
celery_app = Celery("ihome")

#配置
celery_app.config_from_object(config)

#自动搜寻任务
celery_app.autodiscover_tasks(["ihome.tasks.sms"])
