from django.core.exceptions import ValidationError

class CategorySubcategoryMixin:
    category_field_name = 'category'
    subcategory_field_name = 'subcategory'

    def clean(self):
        category = getattr(self, self.category_field_name)
        subcategory = getattr(self, self.subcategory_field_name)

        if subcategory and subcategory.category != category:
            raise ValidationError(f"Subcategory '{subcategory}' does not match the selected category '{category}'.")

        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
