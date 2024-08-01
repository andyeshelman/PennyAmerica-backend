from ninja import ModelSchema, Schema, Field

from expenses.models import Expense
from accounts.schemas import UserSchemaOut

class ExpenseSchemaIn(ModelSchema):
    recurring: str | None = None
    ends_on: str | None = None
    class Meta:
        description = "Schema for creating a new expense"
        model = Expense
        fields = ['name', 'description', 'amount', 'starts_on']
        fields_optional = ['recurring', 'ends_on']

class ExpenseSchemaOut(ModelSchema):
    user: UserSchemaOut
    class Meta:
        description = "Schema for displaying an expense"
        model = Expense
        fields = ['id', 'name', 'description', 'amount', 'recurring', 'starts_on', 'ends_on', 'created_at', 'updated_at']

class CreateSchemaOut(Schema):
    id: int = Field(..., example=1)

    class Meta:
        description = "Schema for the created object output"