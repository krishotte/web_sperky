"""Product Model."""

from config.database import Model
from orator.orm import belongs_to, belongs_to_many


class Product(Model):
    """Product Model."""
    __fillable__ = ['name', 'category_id', 'price']

    @belongs_to('category_id', 'id')
    def category(self):
        from app.Product_category import Product_category

        return Product_category

    @belongs_to_many()
    def materials(self):
        from app.Material import Material
        return Material
