"""A AdminsNewOrderMailable Mailable."""

from masonite.drivers import Mailable
from os import environ


class AdminsNewOrderMailable(Mailable):
    """A AdminsNewOrderMailable Mailable."""

    def __init__(self, to, order):
        """A AdminsNewOrderMailable Initializer."""
        self._to = to
        self.order = order

    def build(self):
        """Logic to handle the job."""
        return (
            self.subject('sperkyodvierky.sk - nová objednávka')
            .send_from(environ['MAIL_FROM_ADDRESS'])
            .reply_to(environ['MAIL_FROM_ADDRESS'])
            .to(self._to)
            .view('email/new_order', {'order': self.order})
        )