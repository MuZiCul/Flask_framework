from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from flask_redis import FlaskRedis
import tenacity
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError

redis_client = FlaskRedis()
db = SQLAlchemy()
mail = Mail()


def create_scoped_session_with_retry(db):
    """
    创建一个带有重试逻辑的scoped_session工厂。
    """

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),  # 尝试次数
        wait=tenacity.wait_random_exponential(multiplier=1, max=60),  # 随机指数退避等待，最大等待60秒
        retry=tenacity.retry_if_exception_type(OperationalError),  # 当遇到OperationalError时重试
        reraise=True,  # 重试结束后仍抛出最后一次异常
    )
    def _create_session():
        return scoped_session(sessionmaker(bind=db.engine))

    return _create_session()


# 提供一个方法来初始化db并应用重试逻辑
def init_db(app):
    db.init_app(app)
    # 替换默认的会话工厂
    db.session_factory = create_scoped_session_with_retry(db)
    db.session = db.create_scoped_session()
