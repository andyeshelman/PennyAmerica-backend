from ninja import Router
from django.http import HttpRequest

from budgets.models import Budget
from budgets.schemas import BudgetSchemaIn, BudgetSchemaOut, BudgetSchemaPatch
from categories.models import Category, Subcategory
from util.schemas import Message

router = Router(tags=['budgets'])

@router.post('', response={201: BudgetSchemaOut, 401: Message})
def create_Budget(request: HttpRequest, budget_in: BudgetSchemaIn):
    if not request.user.is_authenticated:
        return 401, Message("Must be logged in to create budget.")
    else:
        budget_data = budget_in.dict()
        budget_data['category'] = Category.objects.get(id=budget_data['category'])
        if budget_data.get('subcategory'):
            budget_data['subcategory'] = Subcategory.objects.get(id=budget_data['subcategory'])
        else:
            budget_data.pop('subcategory')
        budget = Budget.objects.create(user=request.user, **budget_data)
        return 201, budget

@router.get('', response={200: list[BudgetSchemaOut], 401: Message})
def get_Budget_list(request: HttpRequest):
    if not request.user.is_authenticated:
        return 401, Message("Must be logged in to view budgets.")
    budgets = Budget.objects.filter(user=request.user)
    return 200, budgets

@router.patch('/{budget_id}', response={200: BudgetSchemaOut, frozenset({401, 403, 404}): Message})
def patch_Budget(request: HttpRequest, budget_id: int, budget_diff: BudgetSchemaPatch):
    if not request.user.is_authenticated:
        return 401, Message("Must be logged in to edit budgets.")
    try:
        budget = Budget.objects.select_related('user').get(id=budget_id)
    except Budget.DoesNotExist:
        return 404, Message(f"Budget with id {budget_id} not found.")
    if not request.user == budget.user:
        return 403, Message("Users may only edit their own budgets.")
    for key, value in budget_diff.dict(exclude_unset=True).items():
        setattr(budget, key, value)
    budget.save()
    return 200, budget

@router.delete('/{budget_id}', response={frozenset({200, 401, 403, 404}): Message})
def delete_Budget(request: HttpRequest, budget_id: int):
    if not request.user.is_authenticated:
        return 401, Message("Must be logged in to delete budgets.")
    try:
        budget = Budget.objects.select_related('user').get(id=budget_id)
    except Budget.DoesNotExist:
        return 404, Message(f"Budget with id {budget_id} not found.")
    if not request.user == budget.user:
        return 403, Message("Users may only delete their own budgets.")
    budget.delete()
    return 200, Message("Budget deleted successfully!")