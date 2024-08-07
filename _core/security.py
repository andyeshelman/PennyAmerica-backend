import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from ninja.security import HttpBearer

class JWTAuth(HttpBearer):
    
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(id=payload['user_id'])
            request.user = user
            return user
        except Exception:
            return None