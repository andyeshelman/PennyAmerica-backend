from ninja import Schema, Field

class CreateSchemaOut(Schema):
    id: int = Field(..., example=1)
    class Meta:
        description = "Schema for the created object output"
        
class Message(Schema):
    message: str