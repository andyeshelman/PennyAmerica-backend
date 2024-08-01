from ninja import ModelSchema, Schema, Field

from django.contrib.auth.models import User

class UserSchemaIn(ModelSchema):
    class Meta:
        description = "Schema for creating a new user"
        model = User
        fields = ['username', 'email', 'password']
        
class UserSchemaOut(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "username"]

class CreateSchemaOut(Schema):
    id: int = Field(..., example=1)
    class Meta:
        description = "Schema for the created object output"
        
class LoginSchema(ModelSchema):
    class Meta:
        description = "Schema for logging a user in"
        model = User
        fields = ['username', 'password']