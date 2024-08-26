from django.db import models as m
from django.contrib.auth import get_user_model


class Budget(m.Model):
    class Recurrance(m.TextChoices):
        DAILY = 'D'
        WEEKLY = 'W'
        MONTHLY = 'M'
        YEARLY = 'Y'

    class Category(m.TextChoices):
        LOAN_PAYMENTS = 'loanPayments'
        BANK_FEES = 'bankFees'
        ENTERTAINMENT = 'entertainment'
        FOOD_AND_DRINK = 'foodAndDrink'
        GENERAL_MERCHANDISE = 'generalMerchandise'
        HOME_IMPROVEMENT = 'homeImprovement'
        MEDICAL = 'medical'
        PERSONAL_CARE = 'personalCare'
        GENERAL_SERVICES = 'generalServices'
        GOVERNMENT_AND_NON_PROFIT = 'governmentAndNonProfit'
        TRANSPORTATION = 'transportation'
        TRAVEL = 'travel'
        RENT_AND_UTILITIES = 'rentAndUtilities'
        
    category = m.CharField(max_length=31, choices=Category)
    subcategory = m.CharField(max_length=255, null=True, blank=False)
    amount = m.DecimalField(max_digits=10, decimal_places=2)
    recurring = m.CharField(
        max_length=7,
        choices=Recurrance,
    )
    user = m.ForeignKey(get_user_model(), related_name='budgets', on_delete=m.CASCADE)