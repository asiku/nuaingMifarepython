from flask import session,redirect
from functools import wraps

def ceksess(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'cekcok_login' in session:
            return func(*args,**kwargs)
        return redirect('/loginusr')
    return wrapper
