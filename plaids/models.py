from django.db import models as m
from django.contrib.auth import get_user_model

class Plaid(m.Model):
    access_token = m.CharField(max_length=255)
    item_id = m.CharField(max_length=255)
    user = m.ForeignKey(get_user_model(), related_name='plaids', on_delete=m.CASCADE)