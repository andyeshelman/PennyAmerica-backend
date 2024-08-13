from ninja import Schema, ModelSchema

from django.contrib.auth.models import User

class UserSchemaIn(ModelSchema):
    class Meta:
        description = "Schema for creating a new user"
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        
class UserSchemaOut(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class LoginSchema(ModelSchema):
    class Meta:
        description = "Schema for logging a user in"
        model = User
        fields = ['username', 'password']
        
class PairTokenSchema(Schema):
    refresh: str
    access: str
    def __init__(self, tkn=None, **kw):
        if tkn is not None:
            super().__init__(refresh=str(tkn), access=str(tkn.access_token), **kw)
        else:
            super().__init__(**kw)

class RefreshTokenSchema(Schema):
    refresh: str
    def __init__(self, tkn=None, **kw):
        if tkn is not None:
            super().__init__(token=tkn, **kw)
        else:
            super().__init__(**kw)

class UserIDSchema(Schema):
    user_id: int