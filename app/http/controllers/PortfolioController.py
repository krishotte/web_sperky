"""A PortfolioController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from app.Product_category import Product_category
from app.Material import Material
from app.Product import Product
from masonite import Upload
from pathlib import Path


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
        categories = Product_category.all()
        materials = Material.all()
        category = Product_category.find(request.param('category_id'))
        products = category.products

        serialized_products = self.add_image_path(products.serialize())

        return view.render('portfolio', {
            'products': serialized_products,
            'categories': categories,
            'materials': materials,
            'category_': category,
        })

        return {
            'category': category.serialize(),
            'products': category.products.serialize()
        }

    def show_one_category_and_material(self, request: Request, view: View):
        categories = Product_category.all()
        materials = Material.all()
        category = Product_category.find(request.param('category_id'))
        material = Material.find(request.param('material_id'))
        products = material.products().where('category_id', '=', category.id).get()

        serialized_products = self.add_image_path(products.serialize())

        return view.render('portfolio', {
            'products': serialized_products,
            'categories': categories,
            'materials': materials,
            'category_': category,
        })

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

    def store_product(self, request: Request, view: View, upload: Upload):
        categories = Product_category.all().serialize()
        materials = Material.all().serialize()

        new_product = Product(
            name=request.all()['name'],
            description=request.all()['description'],
            price=request.all()['price'],
        )
        new_product.category().associate(Product_category.where('name', '=', request.all()['category']).first())
        new_product.save()
        print(f'product created, id: {new_product.id}')

        material_ids = []
        for each in request.all().keys():
            if each.startswith('mat_'):
                material_ids.append(int(each[4:]))
        print(f'chosen material_ids: {material_ids}')

        new_product.materials().sync(material_ids)

        saved = self.save_file_to_disk(new_product.id, upload, request)
        print(f'file was saved: {saved}')

        """return view.render('new_product', {
            'categories': categories,
            'materials': materials,
        })"""

        return request.redirect('/admin/product/edit/' + str(new_product.id))

        # return request.all()

    def get_one_product(self, request: Request, view: View):
        product = Product.find(request.param('product_id'))
        categories = Product_category.all()
        materials = Material.all()
        checked_materials = [each.id for each in product.materials]

        images = self.get_files_on_disk(product.id)

        return view.render('edit_product', {
            'product': product.serialize(),
            'categories': categories.serialize(),
            'materials': materials.serialize(),
            'checked_materials': checked_materials,
            'images': images,
        })

    def update_product(self, request: Request, view: View, upload: Upload):
        product_to_update = Product.find(request.param('product_id'))

        product_to_update.name = request.all()['name']
        product_to_update.description = request.all()['description']
        product_to_update.price = request.all()['price']

        product_to_update.category().associate(Product_category.where('name', '=', request.all()['category']).first())
        product_to_update.save()

        material_ids = []
        for each in request.all().keys():
            if each.startswith('mat_'):
                material_ids.append(int(each[4:]))

        product_to_update.materials().sync(material_ids)

        saved = self.save_file_to_disk(product_to_update.id, upload, request)
        print(f'file was saved: {saved}')

        images = self.get_files_on_disk(product_to_update.id)

        categories = Product_category.all()
        materials = Material.all()
        checked_materials = [each.id for each in product_to_update.materials]

        return view.render('edit_product', {
            'product': product_to_update.serialize(),
            'categories': categories.serialize(),
            'materials': materials.serialize(),
            'checked_materials': checked_materials,
            'images': images,
        })

        # return [request.input('name'), request.input('description'), request.input('price')]

    def save_file_to_disk(self, product_id, upload: Upload, request: Request):
        """
        generates folder name and file names
        scans if folder and files exist
        saves file received in request to new file
        :return: True if file was saved
        """
        folder_prefix = 'storage/static/img/'
        folder = folder_prefix + str(product_id).zfill(4)

        product_folder = Path.cwd().joinpath("storage").joinpath("static").joinpath("img").joinpath(str(product_id).zfill(4))
        print(f'product folder: {product_folder}, exists: {product_folder.exists()}')

        if not product_folder.exists():
            product_folder.mkdir()

        for each in product_folder.iterdir():
            print(f' file found: {each.name}')

        file_name_available = False
        counter = 0
        while (not file_name_available) and (counter < 10):
            counter += 1
            # print(f'counter: {counter}')
            name_to_check = f'{str(product_id).zfill(4)}_{str(counter).zfill(2)}.jpg'

            print(f' file {name_to_check} exists: {product_folder.joinpath(name_to_check).exists()}')
            if not product_folder.joinpath(name_to_check).exists():
                file_name_available = True

        if file_name_available:
            try:
                upload.driver('disk').store(request.input("file"), location=folder, filename=name_to_check)
                return True
            except Exception:
                pass

        return False

    def get_files_on_disk(self, product_id):
        product_folder = Path.cwd().joinpath("storage").joinpath("static").joinpath("img").joinpath(str(product_id).zfill(4))
        print(f'product folder: {product_folder}')

        files = ['/static/img/' + str(product_id).zfill(4) + '/' + file.name for file in product_folder.iterdir()]
        print(f'files found: {files}')

        return files

    def add_image_path(self, serialized_products):
        for product in serialized_products:
            id_str = str(product['id']).zfill(4)
            product['image'] = f'/static/img/{id_str}/{id_str}_01.jpg'

        # print(serialized_products)
        return serialized_products
