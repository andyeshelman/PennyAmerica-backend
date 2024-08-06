from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from accounts.schemas import UserSchemaIn, LoginSchema
from util.schemas import CreateSchemaOut, Message

router = Router(tags=['accounts'])

@router.post('/', response={201: CreateSchemaOut})
def create_user(request: HttpRequest, user_in: UserSchemaIn):
    user = User.objects.create_user(**user_in.dict())
    return user

@router.post('/login', response={frozenset({200, 401}): Message})
def login_user(request: HttpRequest, creds: LoginSchema):
    user = authenticate(request, **creds.dict())
    if user is not None:
        login(request, user)
        return 200, Message("Logged in successfully!")
    else:
        return 401, Message("Username and/or password are invalid...")
    
@router.post('/logout', response={200: Message})
def logout_user(request: HttpRequest):
    logout(request)
    return 200, Message("Logged out successfully!")