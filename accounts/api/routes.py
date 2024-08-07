from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from accounts.schemas import UserSchemaIn, LoginSchema
from util.schemas import CreateSchemaOut, Message, Token
from util.token import encode_token

router = Router(tags=['accounts'])

@router.post('/register', response={201: CreateSchemaOut}, auth=None)
def create_user(request: HttpRequest, user_in: UserSchemaIn):
    user = User.objects.create_user(**user_in.dict())
    return user

@router.post('/token', response={200: Token, 401: Message}, auth=None)
def login_user(request: HttpRequest, creds: LoginSchema):
    user = authenticate(request, **creds.dict())
    if user is not None:
        return 200, Token(encode_token(user.id))
    else:
        return 401, Message("Username and/or password are invalid...")
