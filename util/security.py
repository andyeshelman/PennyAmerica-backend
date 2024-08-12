from util.schemas import Message

from functools import wraps

def require_admin(func):
    
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return 403, Message("Admin privileges required...")
        return func(request, *args, **kwargs)

    return wrapper