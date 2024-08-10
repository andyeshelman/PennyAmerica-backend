from django.http import HttpResponseForbidden

from functools import wraps

def require_admin(func):
    
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Admin privileges required...")
        return func(request, *args, **kwargs)

    return wrapper