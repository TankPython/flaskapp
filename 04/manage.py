#coding:utf-8
from flask_migrate import Migrate, MigrateCommand

from ihome import Create_app,db

from flask_script import Manager

app = Create_app("develop") #创建app
manager = Manager(app) #启动的manage文件
Migrate(app,db)  #创建数据库的迁移工具对象

manager.add_command("db",MigrateCommand) #添加迁移命令


if __name__ == '__main__':
    manager.run()


