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

    def show(self, view: View):
        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()
        products = Product.order_by('id', 'desc').get()

        serialized_products = add_image_path(products.serialize())
        serialized_products = add_description_lines(serialized_products)

        return view.render('portfolio', {
            'products': serialized_products,
            'categories': categories,
            'materials': materials,
            'category_': {'id': -1},
            'material_': {'id': -1},
        })

    def show_one_category(self, request: Request, view: View):
        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()
        category = Product_category.find(request.param('category_id'))
        products = category.products().order_by('id', 'desc').get()

        serialized_products = add_image_path(products.serialize())
        serialized_products = add_description_lines(serialized_products)

        return view.render('portfolio', {
            'products': serialized_products,
            'categories': categories,
            'materials': materials,
            'category_': category,
            'material_': {'id': -1},
        })

        return {
            'category': category.serialize(),
            'products': category.products.serialize()
        }

    def show_one_category_and_material(self, request: Request, view: View):
        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()
        category = Product_category.find(request.param('category_id'))
        material = Material.find(request.param('material_id'))
        products = material.products().where('category_id', '=', category.id).order_by('id', 'desc').get()

        serialized_products = add_image_path(products.serialize())
        serialized_products = add_description_lines(serialized_products)

        return view.render('portfolio', {
            'products': serialized_products,
            'categories': categories,
            'materials': materials,
            'category_': category,
            'material_': material,
        })

        return {
            'category': category.serialize(),
            'material': material.serialize(),
            'products': material.products().where('category_id', '=', category.id).get().serialize(),
        }

    def show_one_product(self, request: Request, view: View):
        product = Product.find(request.param('product_id'))
        serialized_product = add_image_path([product.serialize()])[0]
        serialized_product = add_description_lines([serialized_product])[0]
        serialized_product = add_detail_lines([serialized_product])[0]
        files, indexes = get_files_on_disk(request.param('product_id'))
        serialized_product['images'] = files
        serialized_product['indexes'] = indexes

        related_products = product.related_products
        related_products_serialized = add_image_path(related_products.serialize())

        # return serialized_product

        return view.render('product', {
            'product': serialized_product,
            'related_products': related_products_serialized,
        })

    def show_search(self, request: Request, view: View):
        products = Product.order_by('id', 'desc').get()

        filtered_products = []
        for each in products:
            if unidecode(each.name.lower()).find(unidecode(request.all()['search'].lower())) >= 0:
                filtered_products.append(each.serialize())

        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()

        serialized_products = add_image_path(filtered_products)
        serialized_products = add_description_lines(serialized_products)

        # return filtered_products
        return view.render('portfolio', {
            'products': serialized_products,
            'categories': categories,
            'materials': materials,
            'category_': {'id': -1},
            'material_': {'id': -1},
        })


def get_files_on_disk(product_id):
    product_folder = Path.cwd().joinpath("storage").joinpath("static").joinpath("img").joinpath(str(product_id).zfill(4))
    print(f'product folder: {product_folder}')

    if not product_folder.exists():
        product_folder.mkdir()

    files = ['/static/img/' + str(product_id).zfill(4) + '/' + file.name for file in product_folder.iterdir()]
    print(f'files found: {files}')
    indexes = list(range(len(files)))

    return files, indexes


def add_image_path(serialized_products):
    for product in serialized_products:
        id_str = str(product['id']).zfill(4)
        product['image'] = f'/static/img/{id_str}/{id_str}_01.jpg'

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
