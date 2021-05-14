"""A PortfolioController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.response import Response
from masonite.controllers import Controller
from app.Product_category import Product_category
from app.Material import Material
from app.Product import Product
from masonite import Upload
from pathlib import Path
from unidecode import unidecode
from masonite.auth import Auth
from app.Availability import Availability
from os import environ
from masonite.response import Response


class PortfolioController(Controller):
    """PortfolioController Controller Class."""
    # TODO_: implement searching
    # TODO_: display and remember pushed button

    def __init__(self, request: Request):
        """PortfolioController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View, request: Request):
        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()
        # products = Product.order_by('id', 'desc').get()

        # get only products with certain availabilities
        products = Product.with_('variants').where_has(
            'availability',
            lambda q: q.where('name', '<>', 'Vypredané')
        ).order_by('id', 'desc').get()

        serialized_products = add_image_path(products.serialize())
        serialized_products = add_description_lines(serialized_products)

        user = get_user(request)
        settings = get_settings()

        return view.render('portfolio', {
            'products': serialized_products,
            'categories': categories,
            'materials': materials,
            'category_': {'id': -1},
            'material_': {'id': -1},
            'user': user,
            'settings': settings,
        })

    def show_one_category(self, request: Request, view: View):
        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()
        category = Product_category.find(request.param('category_id'))
        # products = category.products().order_by('id', 'desc').get()

        # get only products with certain availabilities
        products = category.products().where_has(
            'availability',
            lambda q: q.where('name', '<>', 'Vypredané')
        ).order_by('id', 'desc').get()
        products.load('variants')

        serialized_products = add_image_path(products.serialize())
        serialized_products = add_description_lines(serialized_products)

        user = get_user(request)
        settings = get_settings()

        return view.render('portfolio', {
            'products': serialized_products,
            'categories': categories,
            'materials': materials,
            'category_': category,
            'material_': {'id': -1},
            'user': user,
            'settings': settings,
        })

    def show_one_category_and_material(self, request: Request, view: View):
        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()
        category = Product_category.find(request.param('category_id'))
        material = Material.find(request.param('material_id'))
        # products = material.products().where('category_id', '=', category.id).order_by('id', 'desc').get()

        # get only products with certain availabilities
        products = material.products().where('category_id', '=', category.id).order_by('id', 'desc').where_has(
            'availability',
            lambda q: q.where('name', '<>', 'Vypredané')
        ).order_by('id', 'desc').get()
        products.load('variants')

        serialized_products = add_image_path(products.serialize())
        serialized_products = add_description_lines(serialized_products)
        user = get_user(request)
        settings = get_settings()

        return view.render('portfolio', {
            'products': serialized_products,
            'categories': categories,
            'materials': materials,
            'category_': category,
            'material_': material,
            'user': user,
            'settings': settings,
        })

    def show_one_product(self, request: Request, view: View, response: Response):
        try:
            product = Product.find(int(request.param('product_id')))
            product.availability
            product.category

            for variant in product.variants:
                variant.load({
                    'availability': Availability.query().where('name', '<>', 'Vypredané')
                })
            print(f' loaded product: {product.serialize()}')

            serialized_product = add_image_path([product.serialize()])[0]
            serialized_product = add_description_lines([serialized_product])[0]
            serialized_product = add_detail_lines([serialized_product])[0]
            serialized_product = add_note_lines([serialized_product])[0]
            files, indexes = get_files_on_disk(request.param('product_id'))
            serialized_product['images'] = files
            serialized_product['indexes'] = indexes

            # related_products = product.related_products
            # get only products with certain availabilities
            related_products = product.related_products().where_has(
                'availability',
                lambda q: q.where('name', '<>', 'Vypredané')
            ).order_by('id', 'desc').get()

            related_products_serialized = add_image_path(related_products.serialize())
            user = get_user(request)
            settings = get_settings()

            return view.render('product', {
                'product': serialized_product,
                'related_products': related_products_serialized,
                'user': user,
                'settings': settings,
            })
        except AttributeError:
            return response.view('does not exist', status=404)
        except ValueError:
            return response.view('bad request', status=400)

    def show_search(self, request: Request, view: View):
        # products = Product.order_by('id', 'desc').get()
        # get only products with certain availabilities
        products = Product.where_has(
            'availability',
            lambda q: q.where('name', '<>', 'Vypredané')
        ).order_by('id', 'desc').get()

        filtered_products = []
        for each in products:
            if unidecode(each.name.lower()).find(unidecode(request.all()['search'].lower())) >= 0:
                filtered_products.append(each.serialize())

        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()

        serialized_products = add_image_path(filtered_products)
        serialized_products = add_description_lines(serialized_products)
        user = get_user(request)
        settings = get_settings()

        # return filtered_products
        return view.render('portfolio', {
            'products': serialized_products,
            'categories': categories,
            'materials': materials,
            'category_': {'id': -1},
            'material_': {'id': -1},
            'user': user,
            'settings': settings,
        })


def get_files_on_disk(product_id):
    product_folder = Path.cwd().joinpath("storage").joinpath("static").joinpath("img_webp").joinpath(str(product_id).zfill(4))
    print(f'product folder: {product_folder}')

    if not product_folder.exists():
        product_folder.mkdir()

    files = ['/static/img_webp/' + str(product_id).zfill(4) + '/' + file.name for file in sorted(product_folder.iterdir())]
    print(f'files found: {files}')
    indexes = list(range(len(files)))

    return files, indexes


def add_image_path(serialized_products):
    for product in serialized_products:
        id_str = str(product['id']).zfill(4)
        product['image'] = f'/static/img_webp/{id_str}/{id_str}_01.webp'

    # print(serialized_products)
    return serialized_products


def add_description_lines(serialized_products):
    for product in serialized_products:
        if (product['description'] != 'None') and (product['description'] is not None) and (product['description'] is not ''):
            product['description_lines'] = product['description'].split('\r\n')
        else:
            product['description_lines'] = ['Popis chýba']

    return serialized_products


def add_detail_lines(serialized_products):
    for product in serialized_products:
        if (product['detail'] != 'None') and (product['detail'] is not None):
            product['detail_lines'] = product['detail'].split('\r\n')
        else:
            product['detail_lines'] = ['Detailný popis chýba']

    return serialized_products


def add_note_lines(serialized_products):
    for product in serialized_products:
        if (product['note'] != 'None') and (product['note'] is not None):
            product['note_lines'] = product['note'].split('\r\n')
        else:
            product['note_lines'] = ['Poznámka chýba']

    return serialized_products


def get_user(request):
    user = {}
    try:
        user['name'] = request.user().name
        user['email'] = request.user().email
        user['role'] = request.user().role.name
    except AttributeError:
        # user = ""
        pass
    print(f' current user: {user}')
    return user


def get_settings():
    try:
        settings = {'fb_chat_id': environ['FB_CHAT_ID']}
    except KeyError:
        settings = {'fb_chat_id': ''}

    return settings
