from django.contrib.auth.models import User
from django.db import models as m


class Expense(m.Model):
    class Recurrance(m.TextChoices):
        DAILY = 'D', "Daily"
        WEEKLY = 'W', "Weekly"
        MONTHLY = 'M', "Monthly"
        YEARLY = 'Y', "Yearly"

    name = m.CharField(max_length=255)
    description = m.TextField(blank=True, null=False, default="")
    amount = m.DecimalField(max_digits=10, decimal_places=2)
    recurring: str | None = m.CharField(
        max_length=20,
        choices=Recurrance.choices,
        null=True,
        default=None,
    )
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)
    starts_on = m.DateTimeField()
    ends_on = m.DateTimeField(null=True, blank=False)
    user = m.ForeignKey(User, related_name='expenses', on_delete=m.CASCADE)