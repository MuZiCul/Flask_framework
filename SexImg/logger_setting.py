import os
import time

from config.exts import db
from config.models import LogModel
import logging
import logging.handlers
from SexImg import config


class DBLogHandler(logging.Handler):
    def emit(self, record):
        level = record.levelname
        message = self.format(record)
        log_entry = LogModel(level=level, content=message)
        try:
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving log to database: {e}")
            logging.getLogger(__name__).error(f"Failed to save log: {e}")


def get_logger():
    local_path = "./logs/"
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    date_str = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))

    logfile = local_path + date_str + ".log"
    file_handler = logging.handlers.TimedRotatingFileHandler(filename=logfile, when="D", interval=1, backupCount=60)
    file_handler.suffix = file_handler.suffix + ".log"
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    file_handler.setFormatter(formatter)
    # 数据库日志处理器
    db_handler = DBLogHandler()

    # 设置日志记录器
    loggers = logging.getLogger(__name__)
    loggers.handlers.clear()
    loggers.addHandler(file_handler)
    loggers.addHandler(db_handler)
    loggers.setLevel(logging.DEBUG)
    return loggers


class logger:
    def __init__(self):
        self.loggers = get_logger()

    def info(self, msg):
        print(msg)
        for i in config.PrintColourList:
            if i in msg:
                msg = msg.replace(i, '')
        self.loggers.info(delErrorGbk(msg))

    def debug(self, msg):
        print(msg)
        for i in config.PrintColourList:
            if i in msg:
                msg = msg.replace(i, '')
        self.loggers.debug(delErrorGbk(msg))

    def warning(self, msg):
        print(msg)
        for i in config.PrintColourList:
            if i in msg:
                msg = msg.replace(i, '')
        self.loggers.warning(delErrorGbk(msg))

    def error(self, msg):
        print(msg)
        for i in config.PrintColourList:
            if i in msg:
                msg = msg.replace(i, '')
        self.loggers.error(delErrorGbk(msg))

    def critical(self, msg):
        print(msg)
        for i in config.PrintColourList:
            if i in msg:
                msg = msg.replace(i, '')
        self.loggers.critical(delErrorGbk(msg))


def delErrorGbk(S):
    backStr = ''
    for i in S:
        try:
            i.encode('gbk')
            backStr += i
        except Exception as e:
            pass
    return backStr
