import os
import uuid
HOSTNAME = os.getenv('MYSQL_HOST', 'mysql_server')
PORT = os.getenv('MYSQL_PORT', '3306')
DATABASE = os.getenv('MYSQL_DB', 'my_url_db')
USERNAME = os.getenv('MYSQL_USER', 'root')
PASSWORD = os.getenv('MYSQL_PWD', '.pass.123word')
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = str(uuid.uuid1())


REDIS_URL = f'redis://{os.getenv("REDIS_HOST", "redis_server")}:{os.getenv("REDIS_PORT", 6379)}'


# 邮箱配置
# MAIL_SERVER = "xxx"
# MAIL_PORT = 123
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# MAIL_DEBUG = True
# MAIL_USERNAME = 'xxx'
# MAIL_PASSWORD = "xxx"
# MAIL_DEFAULT_SENDER = '123456@123.com'
