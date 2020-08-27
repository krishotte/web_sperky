"""Product_category Model."""

from config.database import Model


class Product_category(Model):
    """Product_category Model."""
    __table__ = 'product_categories'
    __fillable__ = ['name']

