from django.db import models as m
from django.contrib.auth import get_user_model

from categories.mixins import CategorySubcategoryMixin

class Budget(m.Model, CategorySubcategoryMixin):
    class Recurrance(m.TextChoices):
        DAILY = 'D'
        WEEKLY = 'W'
        MONTHLY = 'M'
        YEARLY = 'Y'
    
    amount = m.DecimalField(max_digits=10, decimal_places=2)
    recurring = m.CharField(
        max_length=7,
        choices=Recurrance,
    )
    user = m.ForeignKey(get_user_model(), related_name='budgets', on_delete=m.CASCADE)
    category = m.ForeignKey('categories.Category', on_delete=m.PROTECT)
    subcategory = m.ForeignKey('categories.Subcategory', on_delete=m.PROTECT, null=True)