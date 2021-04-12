"""A BlogController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from .PortfolioController import get_user, get_settings


class BlogController(Controller):
    """BlogController Controller Class."""

    def __init__(self, request: Request):
        """BlogController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View):
        pass

    def show_first(self, request: Request, view: View):
        user = get_user(request)

        return view.render('blog/first', {
            'user': user,
            'settings': get_settings(),
        })
