"""User Model."""

from config.database import Model
from orator.orm import belongs_to, has_many


class User(Model):
    """User Model."""

    __fillable__ = ['name', 'email', 'password']

    __auth__ = 'email'

    @belongs_to
    def role(self):
        from app.Role import Role

        return Role

    @has_many
    def addresses(self):
        from app.Address import Address
        return Address.order_by('id', 'asc')

    @has_many
    def orders(self):
        from app.Order import Order

        return Order
