"""A SendAdminsNewUserJob Queue Job."""

from masonite.queues import Queueable
from masonite.request import Request
from masonite import Mail
from app.mailable.AdminsNewUserMailable import AdminsNewUserMailable
from app.User import User
import time


class SendAdminsNewUserJob(Queueable):
    """A SendAdminsNewUserJob Job."""

    def __init__(self, request: Request, mail: Mail):
        """A SendAdminsNewUserJob Constructor."""
        self.request = request
        self.mail = mail

    def handle(self, user_address):
        """Logic to handle the job."""
        admins = User.where('role_id', '=', 1).get()
        print(f' admins: {admins.serialize()}')

        for admin in admins:
            print(f' found admin: {admin.email}')
            # self.mail.mailable(AdminsNewUserMailable(admin.email, user_address)).send()
            self.mail.to(admin.email).subject('sperkyodvierky.sk - nový užívateľ').template('email/new_user',
                                                                                        {'user_address': user_address}).send()
            time.sleep(0.2)
