from ninja import Schema, Field

from typing import TypeVar, Generic

T = TypeVar('T')

class CreateSchemaOut(Schema):
    id: int = Field(..., example=1)
    class Meta:
        description = "Schema for the created object output"
        
class Message(Schema):
    message: str
    def __init__(self, msg=None, **kw):
        if msg is not None:
            super().__init__(message=msg, **kw)
        else:
            super().__init__(**kw)
            
class Token(Schema):
    token: str
    def __init__(self, tkn=None, **kw):
        if tkn is not None:
            super().__init__(token=tkn, **kw)
        else:
            super().__init__(**kw)
            
class Body(Schema, Generic[T]):
    value: T