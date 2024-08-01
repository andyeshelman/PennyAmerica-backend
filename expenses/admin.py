from django.contrib import admin
from expenses.models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'amount',
        'recurring',
        'user',
        'created_at',
        'updated_at',
        'starts_on',
        'ends_on',
    )
    list_filter = ('recurring',)

admin.site.register(Expense, ExpenseAdmin)