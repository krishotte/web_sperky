"""A MainController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from app.Product_category import Product_category


class MainController(Controller):
    """MainController Controller Class."""

    def __init__(self, request: Request):
        """MainController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View):
        categories = Product_category.order_by('id', 'asc').get()

        # return categories.serialize()
        return view.render('main', {'categories': categories})
