# -*- coding: utf-8 -*-
from functools import wraps
from flask import session

def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session["username"] == "admin":
            return f(*args, **kwargs)
        else:
            return "not admin"
    return wrap
