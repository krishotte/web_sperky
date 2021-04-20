"""A AdminsNewUserMailable Mailable."""

from masonite.drivers import Mailable
from os import environ


class AdminsNewUserMailable(Mailable):
    """A AdminsNewUserMailable Mailable."""

    def __init__(self, to, user_address):
        """A AdminsNewUserMailable Initializer."""
        self._to = to
        self.user_address = user_address

    def build(self):
        """Logic to handle the job."""
        return (
            self.subject('sperkyodvierky.sk - nový užívateľ')
            .send_from(environ['MAIL_FROM_ADDRESS'])
            .reply_to(environ['MAIL_FROM_ADDRESS'])
            .to(self._to)
            .view('email/new_user', {'user_address': self.user_address})
        )