from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from ninja_jwt.schema import TokenObtainPairInputSchema, TokenRefreshInputSchema

from accounts.schemas import UserSchemaIn, LoginSchema
from util.schemas import CreateSchemaOut, Message

router = Router(tags=['accounts'])

@router.post('/', response={201: CreateSchemaOut})
def create_user(request: HttpRequest, user_in: UserSchemaIn):
    user = User.objects.create_user(**user_in.dict())
    return user

@router.post('/login', response={frozenset({200, 401}): dict})
def login_user(request: HttpRequest, creds: LoginSchema):
    user = authenticate(request, **creds.dict())
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return 200, {
            'message': "Logged in successfully!",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    else:
        return 401, Message("Username and/or password are invalid.")
    
@router.post('/logout', response={200: Message})
def logout_user(request: HttpRequest):
    logout(request)
    return 200, Message("Logged out successfully!")

@router.post('/token/', response={200: TokenObtainPairInputSchema})
def token_obtain_pair(request: HttpRequest):
    return TokenObtainPairView.as_view()(request)

@router.post('/token/refresh/', response={200: TokenRefreshInputSchema})
def token_refresh(request: HttpRequest):
    return TokenRefreshView.as_view()(request)