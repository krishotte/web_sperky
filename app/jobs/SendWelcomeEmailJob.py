"""A SendWelcomeEmailJob Queue Job."""

from masonite.queues import Queueable
from masonite.request import Request
from masonite import Mail
from app.mailable.WelcomeEmailMailable import WelcomeEmailMailable


class SendWelcomeEmailJob(Queueable):
    """A SendWelcomeEmailJob Job."""

    def __init__(self, request: Request, mail: Mail):
        """A SendWelcomeEmailJob Constructor."""
        self.request = request
        self.mail = mail

    def handle(self, user_address, user_name):
        """Logic to handle the job."""
        self.mail.mailable(WelcomeEmailMailable(user_address, user_name)).send()
