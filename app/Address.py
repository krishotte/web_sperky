"""Address Model."""

# from config.database import Model
from orator.orm import belongs_to
from orator import Model, SoftDeletes


class Address(Model, SoftDeletes):
    """
    Address Model.

    id: integer default: None
    user_id: integer default: None
    street: string(255) default: None
    zip_code: string(255) default: None
    city: string(255) default: None
    name: string(255) default: name
    phone: string(255) default: None
    """
    __fillable__ = ['street', 'zip_code', 'city', 'name', 'phone']
    __dates__ = ['deleted_at']

    @belongs_to
    def user(self):
        from app.User import User
        return User
