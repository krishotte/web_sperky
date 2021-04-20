"""A WelcomeEmailMailable Mailable."""

from masonite.drivers import Mailable
from os import environ


class WelcomeEmailMailable(Mailable):
    """A WelcomeEmailMailable Mailable."""

    def __init__(self, user_address, user_name):
        """A WelcomeEmailMailable Initializer."""
        self._to = user_address
        self.user_name = user_name

    def build(self):
        """Logic to handle the job."""
        return (
            self.subject('Vitajte na sperkyodvierky.sk')  # .to(self._to).view('email/welcome')
            .send_from(environ['MAIL_FROM_ADDRESS'])
            .reply_to(environ['MAIL_FROM_ADDRESS'])
            .to(self._to)
            .view('email/welcome', {'user_name': self.user_name})
            # .view('template')
        )
