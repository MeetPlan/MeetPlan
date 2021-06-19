from functools import wraps

class NotAuthenticatedException(Exception):
    pass

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        #if not request.state.user.admin:
        #    return "<h1>403 - Forbidden</h1><p>You need admin priveleges to access this page", 403
        return func(*args, **kwargs)
    return decorated_view

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        #if not request.state.user.admin:
        #    return "<h1>403 - Forbidden</h1><p>You need admin priveleges to access this page", 403
        return func(*args, **kwargs)
    return decorated_view