from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from ninja_jwt.tokens import RefreshToken, BlacklistedToken
from ninja_jwt.exceptions import TokenError

from accounts.schemas import UserSchemaIn, UserSchemaOut, LoginSchema, BlacklistUserTokensSchema, RefreshTokenSchema, PairTokenSchema
from util.schemas import CreateSchemaOut, Message
from util.security import require_admin

router = Router(tags=['accounts'])

@router.post('/register', response={201: CreateSchemaOut, 400: Message}, auth=None)
def create_user(request: HttpRequest, user_in: UserSchemaIn):
    try:
        user = User.objects.create_user(**user_in.dict())
        return 201, user
    except IntegrityError as e:
        if 'auth_user_username_key' in str(e):
            return 400, Message(detail="Username already exists.")
        raise e

@router.post('/login', response={200: PairTokenSchema, 401: Message}, auth=None)
def login_user(request: HttpRequest, creds: LoginSchema):
    request.session.flush()
    user = authenticate(request, **creds.dict())
    if user is not None:
        login(request, user) 
        refresh = RefreshToken.for_user(user)
        return 200, PairTokenSchema(refresh)
    else:
        return 401, Message("Username and/or password are invalid.")
    
@router.get('/profile', response={200: UserSchemaOut, 404: Message})
def get_user_profile(request):
    try:
        user = request.user
        return 200, user
    except User.DoesNotExist:
        return 404, {"message": "User not found"}

@router.post('/logout', response={200: Message})
def logout_user(request: HttpRequest, refresh_token: RefreshTokenSchema):
    token = RefreshToken(refresh_token.refresh)
    token.blacklist()
    request.session.flush()
    logout(request)
    return 200, Message("Logged out successfully!")

@router.post('/refresh', response={200: PairTokenSchema, frozenset({401, 500}): Message})
def token_refresh(request: HttpRequest, refresh_token: RefreshTokenSchema):
    try:
        refresh = RefreshToken(refresh_token.refresh)
        return 200, PairTokenSchema(refresh)
    except TokenError as e:
        return 401, Message(str(e))
    except Exception as e:
        return 500, Message(str(e))

@router.post('/blacklist_user_tokens', response={frozenset({200, 403, 404, 500}): Message})
@require_admin
def blacklist_user_tokens(request: HttpRequest, payload: BlacklistUserTokensSchema):
    try:
        target_user = User.objects.get(id=payload.user_id)
        tokens = target_user.outstandingtoken_set.all()
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token_id=token.id)      
        return 200, Message("All tokens for the user have been blacklisted.")  
    except User.DoesNotExist:
        return 404, Message("User not found.")
    except Exception as e:
        return 500, Message(str(e))