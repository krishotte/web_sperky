"""Address Model."""

from config.database import Model
from orator.orm import belongs_to


class Address(Model):
    """Address Model."""
    __fillable__ = ['street', 'zip_code', 'city']

    @belongs_to
    def user(self):
        from app.User import User

        return User