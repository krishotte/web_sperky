"""A DashboardController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from .PortfolioController import get_user


class DashboardController(Controller):
    """DashboardController Controller Class."""

    def __init__(self, request: Request):
        """DashboardController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, request: Request, view: View):
        user = get_user(request)

        return view.render('dash/menu', {
            'user': user,
        })

    def show_profile(self, request: Request, view: View):
        user = get_user(request)
        # print(f' environ: {request.environ}')
        print(f' caller: {request.header("HTTP_REFERER")}')

        return view.render('dash/profile', {
            'user': user,
        })

    def show_orders(self, request: Request, view: View):
        user = get_user(request)
        return view.render('dash/orders', {
            'user': user,
        })
