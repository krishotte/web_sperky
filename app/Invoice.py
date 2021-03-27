"""Invoice Model."""

from config.database import Model
from orator.orm import belongs_to


class Invoice(Model):
    """
    Invoice Model.

    id: integer default: None
    prefix: string(255) default: None
    year: integer default: None
    number: integer default: None
    variable_symbol: string(255) default: None
    issue_date: date default: None
    due_date: date default: None
    valid: boolean default: True
    """
    __fillable__ = ['prefix', 'year', 'number', 'variable_symbol', 'issue_date', 'due_date', 'valid']

    @belongs_to
    def order(self):
        from app.Order import Order
        return Order
