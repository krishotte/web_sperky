"""A TestController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from .PortfolioController import get_user
from masonite import Mail, Queue
from app.mailable.WelcomeEmailMailable import WelcomeEmailMailable
from app.jobs.SendWelcomeEmailJob import SendWelcomeEmailJob
from app.jobs.SendAdminsNewUserJob import SendAdminsNewUserJob
from app.jobs.SendAdminsNewOrderJob import SendAdminsNewOrderJob
from os import environ
from app.User import User
from app.Order import Order
from threading import Thread
import time


class TestController(Controller):
    """TestController Controller Class."""

    def __init__(self, request: Request):
        """TestController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, request: Request, view: View):
        user = get_user(request)

        return view.render('admin/test/main', {
            'user': user,
        })

    def send_welcome_email(self, request: Request, mail: Mail):
        user = get_user(request)
        print(f' sending welcome email to: {user["email"]}')

        mail.mailable(WelcomeEmailMailable(user['email'], user['name'])).send()
        # mail.to(user['email']).template('email/welcome').subject('Vitajte na sperkyodvierky.sk').send()

        return request.redirect('/admin/test')

    def send_welcome_email_queue(self, request: Request, queue: Queue):
        user = get_user(request)
        print(f' sending welcome email to: {user["email"]}, through queue')
        queue.push(SendWelcomeEmailJob, args=[user['email'], user['name']])

        return request.redirect('/admin/test')

    def send_more_welcome_email(self, request: Request, mail: Mail):
        user = get_user(request)
        print(f' sending more emails to you...')

        emails = [
            WelcomeEmailMailable(user['email'], f"{user['name']} - 1"),
            WelcomeEmailMailable(user['email'], f"{user['name']} - 2"),
            WelcomeEmailMailable(user['email'], f"{user['name']} - 3"),
        ]
        thr1 = Thread(target=send_more_welcome_emails, args=[mail, emails])
        thr1.start()
        print(f' thread started, redirecting')

        return request.redirect('/admin/test')


    def send_admins_new_user(self, request: Request, queue: Queue):
        user = User.find(4)  # {'email': request.input('user')}
        queue.push(SendAdminsNewUserJob, args=[user.email])

        return request.redirect('/admin/test')

    def send_admins_new_order(self, request: Request, queue: Queue):
        order = Order.find(32)
        order.user

        queue.push(SendAdminsNewOrderJob, args=[order.serialize()])

        return request.redirect('/admin/test')


def send_more_welcome_emails(mail, emails):
    for i, email in enumerate(emails):
        print(f' sending welcome email: {i}')
        # mail.mailable(WelcomeEmailMailable(user['email'], user['name'])).send()
        mail.mailable(email).send()
        time.sleep(2)
