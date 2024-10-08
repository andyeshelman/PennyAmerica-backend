# Generated by Django 5.1 on 2024-08-26 23:59

from django.db import migrations

def load_categories(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    Subcategory = apps.get_model('categories', 'Subcategory')
    with open('categories/category_data.txt') as file:
        data = [line.split(',', 2) for line in file]
        cats = {}
        for cat in {row[0] for row in data}:
            cats[cat] = Category.objects.create(name=cat)
        for row in data:
            subcat = row[1][len(row[0]) + 1:]
            desc = row[2].replace('"','').strip()
            Subcategory.objects.create(
                name=subcat,
                description=desc,
                category=cats[row[0]]
            )

class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_categories),
    ]
