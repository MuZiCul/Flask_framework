import os
import uuid
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件的绝对路径
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SCHEDULER_TIMEZONE = 'Asia/Shanghai'
SECRET_KEY = str(uuid.uuid1())

# 邮箱配置
MAIL_SERVER = "xxx"
MAIL_PORT = 123
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = 'xxx'
MAIL_PASSWORD = "xxx"
MAIL_DEFAULT_SENDER = '123456@123.com'
