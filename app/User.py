"""User Model."""

from config.database import Model
from orator.orm import belongs_to, has_many
from masonite.auth import MustVerifyEmail
from app.tools.SvkMustVerifyEmail import SvkMustVerifyEmail


class User(Model, SvkMustVerifyEmail):
    """User Model."""

    __fillable__ = ['name', 'email', 'password']

    __auth__ = 'email'
    __dates__ = ['created_at', 'updated_at', 'verified_at']

    def get_date_format(self):
        return "%Y-%m-%d"

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
