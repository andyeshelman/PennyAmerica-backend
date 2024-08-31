from ninja import Router
from django.http import HttpRequest

from categories.models import Category
from categories.schemas import CategorySchema

router = Router(tags=['categories'])

@router.get('/all', response={200: list[CategorySchema]}, auth=None)
def get_categories(request: HttpRequest):
    return 200, Category.objects.prefetch_related('subcategories').all()