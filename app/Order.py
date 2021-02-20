"""Order Model."""

from config.database import Model
from orator.orm import belongs_to, belongs_to_many


class Order(Model):
    """Order Model."""
    __fillable__ = ['total_price']

    @belongs_to
    def user(self):
        from app.User import User
        return User

    @belongs_to_many(with_pivot=['product_count', 'unit_price'])
    def products(self):
        from app.Product import Product
        return Product

    @belongs_to
    def order_state(self):
        from app.OrderState import OrderState
        return OrderState

    @belongs_to
    def shipping(self):
        from app.Shipping import Shipping
        return Shipping

    @belongs_to
    def address(self):
        from app.Address import Address
        return Address
