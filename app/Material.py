"""Material Model."""

from config.database import Model
from orator.orm import belongs_to_many


class Material(Model):
    """Material Model."""
    __fillable__ = ['name']

    @belongs_to_many()
    def products(self):
        from app.Product import Product
        return Product
