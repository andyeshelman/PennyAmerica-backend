from ninja import Router
from django.http import HttpRequest, HttpResponse

from expenses.models import Expense
from expenses.schemas import ExpenseSchemaIn, ExpenseSchemaOut

router = Router(tags=['expenses'])

@router.post('/', response={201: ExpenseSchemaOut})
def create_expense(request: HttpRequest, expense_in: ExpenseSchemaIn):
    print(request.POST.dict())
    if not request.user.is_authenticated:
        return HttpResponse("Must be logged in to create expense", status=401)
    else:
        print(expense_in.dict(exclude_unset=False))
        expense = Expense.objects.create(user=request.user, **expense_in.dict())
        return expense

@router.get('/', response=list[ExpenseSchemaOut])
def get_expense_list(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponse("Must be logged in to view expenses", status=401)
    expenses = Expense.objects.filter(user=request.user)
    return expenses