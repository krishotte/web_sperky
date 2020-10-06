"""Order Model."""

from config.database import Model
from orator.orm import belongs_to, belongs_to_many


class Order(Model):
    """Order Model."""
    __fillable__ = ['shipping_price', 'total_price']

    @belongs_to
    def user(self):
        from app.User import User

        return User

    @belongs_to_many
    def products(self):
        from app.Product import Product

        return Product