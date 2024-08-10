from ninja import Router, errors
from ninja.responses import Response
from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja_jwt.tokens import RefreshToken, BlacklistedToken
from ninja_jwt.exceptions import TokenError

from accounts.schemas import UserSchemaIn, LoginSchema, BlacklistUserTokensSchema, RefreshTokenSchema, PairTokenSchema
from util.schemas import CreateSchemaOut, Message
from util.security import require_admin

router = Router(tags=['accounts'])

@router.post('/', response={201: CreateSchemaOut}, auth=None)
def create_user(request: HttpRequest, user_in: UserSchemaIn):
    user = User.objects.create_user(**user_in.dict())
    return user

@router.post('/login', response={200: PairTokenSchema, 401: Message}, auth=None)
def login_user(request: HttpRequest, creds: LoginSchema):
    user = authenticate(request, **creds.dict())
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return 200, PairTokenSchema(refresh)
    else:
        return 401, Message("Username and/or password are invalid.")


@router.post('/logout', response={200: Message})
def logout_user(request: HttpRequest, refresh_token: RefreshTokenSchema):
    token = RefreshToken(refresh_token.refresh)
    token.blacklist()
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
def blacklist_user_tokens(request, user_id: int):
    try:
        target_user = User.objects.get(id=user_id)
        tokens = target_user.outstandingtoken_set.all()
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token_id=token.id)
        return 200, Message("All tokens for the user have been blacklisted.")
    except User.DoesNotExist:
        return 404, Message("User not found...")
    except Exception as e:
        return 500, Message(str(e))