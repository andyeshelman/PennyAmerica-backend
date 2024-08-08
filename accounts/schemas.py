from ninja import ModelSchema

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