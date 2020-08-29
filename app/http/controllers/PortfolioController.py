"""A PortfolioController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from app.Product_category import Product_category
from app.Material import Material


class PortfolioController(Controller):
    """PortfolioController Controller Class."""

    def __init__(self, request: Request):
        """PortfolioController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View):
        return view.render('menu')

    def show_one_category(self, request: Request, view: View):
        category = Product_category.find(request.param('category_id'))

        return {
            'category': category.serialize(),
            'products': category.products.serialize()
        }

    def show_one_category_and_material(self, request: Request, view: View):
        category = Product_category.find(request.param('category_id'))
        material = Material.find(request.param('material_id'))

        return {
            'category': category.serialize(),
            'material': material.serialize(),
            'products': material.products().where('category_id', '=', category.id).get().serialize(),
        }
