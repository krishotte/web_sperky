"""OrderState Model."""

from config.database import Model


class OrderState(Model):
    """
    OrderState Model.

    id: integer default: None
    name: string(255) default: None
    phase: integer default: None
    """
    __fillable__ = ['name', 'phase']
    __table__ = 'order_states'
