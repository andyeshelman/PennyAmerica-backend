from ninja import ModelSchema

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

class BudgetSchemaPatch(ModelSchema):
    class Meta:
        model = Budget
        fields = ['category', 'subcategory', 'amount', 'recurring']
        fields_optional = '__all__'
