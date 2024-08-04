from ninja import ModelSchema

from expenses.models import Expense
from accounts.schemas import UserSchemaOut

class ExpenseSchemaIn(ModelSchema):
    class Meta:
        description = "Schema for creating a new expense"
        model = Expense
        fields = ['name', 'description', 'amount', 'recurring', 'starts_on', 'ends_on']
        fields_optional = ['recurring', 'ends_on']

class ExpenseSchemaOut(ModelSchema):
    user: UserSchemaOut
    class Meta:
        description = "Schema for displaying an expense"
        model = Expense
        fields = '__all__'

class ExpenseSchemaPatch(ModelSchema):
    class Meta:
        model = Expense
        fields = ['name', 'description', 'amount', 'recurring', 'starts_on', 'ends_on']
        fields_optional = '__all__'
