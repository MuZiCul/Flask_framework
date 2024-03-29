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
                print('login_required：', str(e))
                flash(str(e))
                session.clear()
                return render_template('login.html')
        else:
            return redirect(url_for('user.login'))
    return wrapper
