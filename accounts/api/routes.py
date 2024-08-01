from ninja import Router
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from http import HTTPStatus

from accounts.schemas import UserSchemaIn, CreateSchemaOut, LoginSchema

router = Router(tags=['accounts'])

@router.post('/', response={201: CreateSchemaOut})
def create_user(request: HttpRequest, user_in: UserSchemaIn):
    user = User.objects.create_user(**user_in.dict())
    return user

@router.post('/login')
def login_user(request: HttpRequest, creds: LoginSchema):
    user = authenticate(request, **creds.dict())
    if user is not None:
        login(request, user)
        return HttpResponse(status=HTTPStatus.OK)
    else:
        return HttpResponse(status=HTTPStatus.UNAUTHORIZED)
    
@router.post('/logout')
def logout_user(request: HttpRequest):
    logout(request)