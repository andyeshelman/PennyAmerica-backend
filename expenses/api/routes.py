from ninja import Router
from django.http import HttpRequest

from expenses.models import Expense
from expenses.schemas import ExpenseSchemaIn, ExpenseSchemaOut, ExpenseSchemaPatch
from util.schemas import Message

router = Router(tags=['expenses'])

@router.post('', response={201: ExpenseSchemaOut, 401: Message})
def create_expense(request: HttpRequest, expense_in: ExpenseSchemaIn):
    if not request.user.is_authenticated:
        return 401, Message("Must be logged in to create expense.")
    else:
        expense = Expense.objects.create(user=request.user, **expense_in.dict())
        return 201, expense

@router.get('', response={200: list[ExpenseSchemaOut], 401: Message})
def get_expense_list(request: HttpRequest):
    if not request.user.is_authenticated:
        return 401, Message("Must be logged in to view expenses.")
    expenses = Expense.objects.filter(user=request.user)
    return 200, expenses

@router.patch('/{expense_id}', response={200: ExpenseSchemaOut, frozenset({401, 403, 404}): Message})
def patch_expense(request: HttpRequest, expense_id: int, expense_diff: ExpenseSchemaPatch):
    if not request.user.is_authenticated:
        return 401, Message("Must be logged in to edit expenses.")
    try:
        expense = Expense.objects.select_related('user').get(id=expense_id)
    except Expense.DoesNotExist:
        return 404, Message(f"Expense with id {expense_id} not found.")
    if not request.user == expense.user:
        return 403, Message("Users may only edit their own expenses.")
    for key, value in expense_diff.dict(exclude_unset=True).items():
        setattr(expense, key, value)
    expense.save()
    return 200, expense

@router.delete('/{expense_id}', response={frozenset({200, 401, 403, 404}): Message})
def delete_expense(request: HttpRequest, expense_id: int):
    if not request.user.is_authenticated:
        return 401, Message("Must be logged in to delete expenses.")
    try:
        expense = Expense.objects.select_related('user').get(id=expense_id)
    except Expense.DoesNotExist:
        return 404, Message(f"Expense with id {expense_id} not found.")
    if not request.user == expense.user:
        return 403, Message("Users may only delete their own expenses.")
    expense.delete()
    return 200, Message("Expense deleted successfully!")