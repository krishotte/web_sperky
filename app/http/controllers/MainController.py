"""A MainController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from app.Product_category import Product_category
from .PortfolioController import get_user


class MainController(Controller):
    """MainController Controller Class."""

    def __init__(self, request: Request):
        """MainController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View, request: Request):
        categories = Product_category.order_by('id', 'asc').get()

        user = get_user(request)
        print(f' logged in user: {user}')

        # return categories.serialize()
        return view.render('main', {
            'categories': categories,
            'user': user,
        })

    def show_contacts(self, request: Request, view: View):
        user = get_user(request)

        return view.render('about/contacts', {
            'user': user,
        })
