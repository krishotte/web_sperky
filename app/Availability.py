"""Availability Model."""

from config.database import Model


class Availability(Model):
    """
    Availability Model.

    id: integer default: None
    name: string(255) default: None
    visual_class: string(255) default: None
    """
    __fillable__ = ['name', 'visual_class']
