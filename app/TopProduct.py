"""TopProduct Model."""

from config.database import Model
from orator.orm import belongs_to


class TopProduct(Model):
    """TopProduct Model."""
    __table__ = 'top_products'

    @belongs_to
    def product(self):
        from app.Product import Product
        return Product
