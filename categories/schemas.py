from ninja import Schema

class SubcategorySchema(Schema):
    id: int
    name: str
    description: str

class CategorySchema(Schema):
    id: int
    name: str
    subcategories: list[SubcategorySchema]