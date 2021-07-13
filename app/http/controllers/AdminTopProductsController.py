"""A AdminTopProductsController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from app.TopProduct import TopProduct
from .PortfolioController import get_user, add_image_path, get_settings
from app.Product import Product


class AdminTopProductsController(Controller):
    """AdminTopProductsController Controller Class."""

    def __init__(self, request: Request):
        """AdminTopProductsController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, request: Request, view: View):
        top_products = TopProduct.order_by('id', 'asc').get()
        top_products.load('product')
        # print(f' top products: {top_products.serialize()}')

        for top_product in top_products:
            id_str = str(top_product.product.id).zfill(4)
            top_product.image = f'/static/img_webp/{id_str}/{id_str}_01.webp'

        print(f' top products with images: {top_products.serialize()}')

        user = get_user(request)

        return view.render('admin/top_products/setup', {
            'user': user,
            'top_products': top_products,
            'settings': get_settings(),
        })

    def choose_new(self, request: Request, view: View):
        user = get_user(request)

        products = Product.order_by('id', 'desc').get()
        serialized_products = add_image_path(products.serialize())

        form_action = '/admin/top_product/create'

        return view.render('admin/top_products/choose_one', {
            'user': user,
            'products': serialized_products,
            'form_action': form_action,
            'settings': get_settings(),
        })

    def create_new(self, request: Request):
        product = Product.find(request.input('product_id'))
        print(f' chosen product: {product.serialize()}')

        new_top_product = TopProduct()
        new_top_product.product().associate(product)
        new_top_product.save()

        return request.redirect('/admin/top_products')

    def show_existing(self, request: Request, view: View):
        user = get_user(request)
        top_product_id = request.input('top_product_id')

        products = Product.order_by('id', 'desc').get()
        serialized_products = add_image_path(products.serialize())

        form_action = '/admin/top_product/update'

        return view.render('admin/top_products/choose_one', {
            'user': user,
            'products': serialized_products,
            'form_action': form_action,
            'top_product_id': top_product_id,
            'settings': get_settings(),
        })

    def update_existing(self, request: Request):
        top_product_to_modify = TopProduct.find(request.input('top_product_id'))
        print(f' modifying top product: {top_product_to_modify.serialize()}')

        product = Product.find(request.input('product_id'))
        top_product_to_modify.product().associate(product)
        top_product_to_modify.save()

        return request.redirect('/admin/top_products')

    def delete_existing(self, request: Request):
        top_product_to_delete = TopProduct.find(request.input('top_product_id'))
        top_product_to_delete.product
        print(f' deleting top product: {top_product_to_delete.serialize()}')
        top_product_to_delete.delete()

        return request.redirect('/admin/top_products')
