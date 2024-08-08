from ninja import Router, errors
from ninja.responses import Response
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from ninja_jwt.schema import TokenObtainPairInputSchema, TokenRefreshInputSchema

from accounts.schemas import UserSchemaIn, LoginSchema, BlacklistUserTokensSchema 
from util.schemas import CreateSchemaOut, Message

router = Router(tags=['accounts'])

def admin_required(request):
    if not request.user.is_authenticated:
        raise errors.HttpError(403, "Authentication required")
    if not request.user.is_staff:
        raise errors.HttpError(403, "Admin privileges required")
    return request.user

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
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({"error": "Authorization header is missing or invalid"}, status=400)
    try:
        token_str = auth_header.split(' ')[1]
        token = RefreshToken(token_str)
        token.blacklist()
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    logout(request)
    return 200, Message("Logged out successfully!")

@router.post('/token', response={200: TokenObtainPairInputSchema})
def token_obtain_pair(request: HttpRequest):
    return TokenObtainPairView.as_view()(request)

@router.post('/token/refresh', response={200: TokenRefreshInputSchema})
def token_refresh(request: HttpRequest):
    return TokenRefreshView.as_view()(request)

@router.post('/blacklist_user_tokens', response={200: Message})
def blacklist_user_tokens(request, payload: BlacklistUserTokensSchema):
    admin_required(request)
    try:
        user_id = payload.user_id
        target_user = User.objects.get(id=user_id)
        tokens = OutstandingToken.objects.filter(user=target_user)
        for token in tokens:
            BlacklistedToken.objects.create(token=token)
        return 200, Message("All tokens for the user have been blacklisted.")
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)