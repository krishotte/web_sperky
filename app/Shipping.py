"""Shipping Model."""

from config.database import Model


class Shipping(Model):
    """
    Shipping Model.

    id: integer default: None
    name: string(255) default: None
    price: float default: None
    """
    __fillable__ = ['name', 'price']
