"""Product_category Model."""

from config.database import Model
from orator.orm import has_many


class Product_category(Model):
    """Product_category Model."""
    __table__ = 'categories'
    __fillable__ = ['name']

    @has_many  # ('category_id', 'id')
    def products(self):
        from app.Product import Product

        return Product

