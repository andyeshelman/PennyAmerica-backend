from django.db import models as m

class Category(m.Model):
    name = m.CharField(max_length=63, unique=True)

class Subcategory(m.Model):
    name = m.CharField(max_length=63)
    description = m.TextField(blank=True, null=False, default="")
    category = m.ForeignKey(Category, related_name='subcategories', on_delete=m.CASCADE)
    
    class Meta:
        unique_together = 'name', 'category'