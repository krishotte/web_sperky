"""User Model."""

from config.database import Model
from orator.orm import belongs_to


class User(Model):
    """User Model."""

    __fillable__ = ['name', 'email', 'password']

    __auth__ = 'email'

    @belongs_to
    def role(self):
        from app.Role import Role

        return Role
