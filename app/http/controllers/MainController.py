"""A MainController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from app.Product_category import Product_category
from .PortfolioController import get_user, get_settings
from app.TopProduct import TopProduct


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

        top_products = TopProduct.order_by('id', 'asc').get()
        for top_product in top_products:
            id_str = str(top_product.product.id).zfill(4)
            top_product.image = f'/static/img_webp/{id_str}/{id_str}_01.webp'

        user = get_user(request)
        print(f' logged in user: {user}')

        # return categories.serialize()
        return view.render('main', {
            'categories': categories,
            'user': user,
            'top_products': top_products,
            'settings': get_settings(),
        })

    def show_contacts(self, request: Request, view: View):
        user = get_user(request)

        return view.render('about/contacts', {
            'user': user,
            'settings': get_settings(),
        })

    def show_conditions(self, request: Request, view: View):
        user = get_user(request)

        return view.render('about/obchodne_podmienky', {
            'user': user,
            'settings': get_settings(),
        })
