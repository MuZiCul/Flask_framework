from config.exts import redis_client, db
from config.models import UserModel


def PollingUserOnline():
    online_users = redis_client.smembers('online_userid')
    for i in online_users:
        if not redis_client.keys(i):
            redis_client.srem('online_userid', i)
            id_ = str(i, encoding='utf-8').split('_')[2]
            user = UserModel.query.filter_by(id=id_).first()
            user.online = 0
            redis_client.delete(f'online_userid_{user.id}', f'user_id_{user.id}')
            db.session.commit()
