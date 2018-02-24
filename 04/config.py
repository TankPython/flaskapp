#coding:utf-8
import redis

class Config():   #笔记
    SECRET_KEY="kdjisofjdk;ddfge"
    #数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/db_python04"
    #设置自动跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #redis
    REDIS_HOST="127.0.0.1"
    REDIS_PORT="6379"
    #flask—session
    SESSION_TYPE="redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期，单位秒

class Developconfig(Config):
    DEBUG = True   #笔记

"""1.配置文件；公用配置：数据库/redis/flask-session配置
    工厂模式，不同的模式，配置信息不一样;但是都继承了一个公用的配置；"""

config_map={
    "develop":Developconfig
}