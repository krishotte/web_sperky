"""A PortfolioController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from app.Product_category import Product_category
from app.Material import Material
from app.Product import Product


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

    def empty_product(self, view: View):
        categories = Product_category.all().serialize()
        materials = Material.all().serialize()

        return view.render('new_product', {
            'categories': categories,
            'materials': materials,
        })

    def store_product(self, request: Request, view: View):
        categories = Product_category.all().serialize()
        materials = Material.all().serialize()

        new_product = Product(
            name=request.all()['name'],
            description=request.all()['description'],
            price=request.all()['price'],
        )
        new_product.category().associate(Product_category.where('name', '=', request.all()['category']).first())
        new_product.save()

        material_ids = []
        for each in request.all().keys():
            if each.startswith('mat_'):
                material_ids.append(int(each[4:]))
        print(f'chosen material_ids: {material_ids}')

        new_product.materials().sync(material_ids)

        return view.render('new_product', {
            'categories': categories,
            'materials': materials,
        })

        # return request.all()
