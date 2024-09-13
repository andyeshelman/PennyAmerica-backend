from ninja import ModelSchema, Schema

from budgets.models import Budget
from accounts.schemas import UserSchemaOut

class BudgetSchemaIn(ModelSchema):
    class Meta:
        model = Budget
        fields = ['category', 'subcategory', 'amount', 'recurring']
        fields_optional = ['subcategory']

class BudgetSchemaOut(ModelSchema):
    user: UserSchemaOut
    class Meta:
        model = Budget
        fields = '__all__'

class BudgetSchemaPatch(Schema):
    amount: float | None = None
    recurring: str | None = None
    category: int | None = None
    subcategory: int | None = None
