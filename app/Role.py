"""Role Model."""

from config.database import Model
from orator.orm import has_many


class Role(Model):
    """Role Model."""
    __fillable__ = ['name']

    @has_many
    def users(self):
        from app.User import User

        return User
