"""Variant Model."""

from config.database import Model
from orator.orm import belongs_to


class Variant(Model):
    """Variant Model."""
    __fillable__ = ['name', 'price', 'image']

    @belongs_to
    def product(self):
        from app.Product import Product
        return Product

    @belongs_to
    def availability(self):
        from app.Availability import Availability
        return Availability
