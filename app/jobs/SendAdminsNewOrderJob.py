"""A SendAdminsNewOrderJob Queue Job."""

from masonite.queues import Queueable
from masonite.request import Request
from masonite import Mail
from app.mailable.AdminsNewOrderMailable import AdminsNewOrderMailable
from app.User import User


class SendAdminsNewOrderJob(Queueable):
    """A SendAdminsNewOrderJob Job."""

    def __init__(self, request: Request, mail: Mail):
        """A SendAdminsNewOrderJob Constructor."""
        self.request = request
        self.mail = mail

    def handle(self, order):
        """Logic to handle the job."""
        admins = User.where('role_id', '=', 1).get()

        for admin in admins:
            print(f' found admin: {admin.email}')
            self.mail.mailable(AdminsNewOrderMailable(admin.email, order)).send()
