import time

from flask import g, redirect, url_for, session, render_template, flash
from functools import wraps


def login_required(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            try:
                print(g.user.id)
                return fun(*args, **kwargs)
            except Exception as e:
                print('！！！！！！！！！出现异常：', str(e))
                flash(str(e))
                session.clear()
                return render_template('login.html')
        else:
            return redirect(url_for('user.login'))
    return wrapper


def throttle(interval=10):  # 默认间隔时间为10秒
    """
    装饰器，限制函数在指定时间内只能被调用一次。
    :param interval: 限制调用的最小时间间隔（秒）
    """

    def decorator(func):
        last_call_time = time.time() - interval  # 初始化为interval秒前

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call_time
            current_time = time.time()
            if current_time - last_call_time >= interval:
                last_call_time = current_time
                return func(*args, **kwargs)
            else:
                print(f"Function '{func.__name__}' was throttled. Last call was {interval} seconds ago.")

        return wrapper

    return decorator