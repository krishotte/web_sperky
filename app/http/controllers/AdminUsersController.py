"""A AdminUsersController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from .PortfolioController import get_user, get_settings
from app.User import User


class AdminUsersController(Controller):
    """AdminUsersController Controller Class."""

    def __init__(self, request: Request):
        """AdminUsersController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View):
        pass

    def show_all_users(self, request: Request, view: View):
        user = get_user(request)

        users = User.order_by('id', 'desc').get()
        users.load('role')

        return view.render('admin/users/all', {
            'user': user,
            'users': users.serialize(),
            'settings': get_settings(),
        })
