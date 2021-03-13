"""A EditPortfolioController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.response import Response
from masonite.controllers import Controller
from app.Product_category import Product_category
from app.Material import Material
from app.Product import Product
from masonite import Upload, Queue
from pathlib import Path
from .PortfolioController import get_files_on_disk, add_image_path, add_description_lines
from os import remove
from app.Availability import Availability
from app.jobs.RestartWebserverJob import RestartWebserverJob
from app.Variant import Variant


class EditPortfolioController(Controller):
    """EditPortfolioController Controller Class."""
    # TODO_: add field for detailed description in product create and edit

    def __init__(self, request: Request):
        """EditPortfolioController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View):
        pass

    def empty_product(self, view: View, request: Request):
        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()
        user = self._get_user(request)

        return view.render('admin.new_product', {
            'categories': categories,
            'materials': materials,
            'user': user,
        })

    def store_product(self, request: Request, view: View, upload: Upload):
        # categories = Product_category.all().serialize()
        # materials = Material.all().serialize()

        # print(f' request: {request.all()}')
        new_product = Product(
            name=request.all()['name'],
            description=request.all()['description'],
            price=request.all()['price'],
            detail=request.all()['detail'],
            note=request.all()['note'],
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

        saved = self._save_file_to_disk(new_product.id, upload, request)
        print(f'file was saved: {saved}')

        """return view.render('new_product', {
            'categories': categories,
            'materials': materials,
        })"""

        return request.redirect('/admin/product/edit/' + str(new_product.id))

        # return request.all()

    def get_one_product(self, request: Request, view: View):
        product = Product.find(request.param('product_id'))
        product.availability
        product.variants
        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()
        checked_materials = [each.id for each in product.materials]

        availabilities = Availability.order_by('id', 'asc').get()

        images, indexes = get_files_on_disk(product.id)

        related_products = product.related_products
        related_products_serialized = add_image_path(related_products.serialize())
        user = self._get_user(request)

        # return product
        return view.render('admin.edit_product', {
            'product': product.serialize(),
            'categories': categories.serialize(),
            'materials': materials.serialize(),
            'checked_materials': checked_materials,
            'images': images,
            'related_products': related_products_serialized,
            'user': user,
            'availabilities': availabilities,
        })

    def get_all_products(self, view: View, request: Request):
        products = Product.order_by('id', 'desc').get()
        products.load('availability')
        serialized_products = add_image_path(products.serialize())
        serialized_products = add_description_lines(serialized_products)

        user = self._get_user(request)
        print(f' logged in user: {user}')

        return view.render('admin.edit_portfolio', {
            'products': serialized_products,
            'categories': [],
            'materials': [],
            'user': user,

        })

    def update_product(self, request: Request, view: View, upload: Upload):
        product_to_update = Product.find(request.param('product_id'))

        product_to_update.name = request.all()['name']
        product_to_update.description = request.all()['description']
        product_to_update.price = request.all()['price']
        product_to_update.detail = request.all()['detail']
        product_to_update.note = request.all()['note']

        product_to_update.category().associate(Product_category.where('name', '=', request.all()['category']).first())
        product_to_update.availability().associate(Availability.where('name', '=', request.input('availability')).first())

        product_to_update.save()

        material_ids = []
        for each in request.all().keys():
            if each.startswith('mat_'):
                material_ids.append(int(each[4:]))

        product_to_update.materials().sync(material_ids)

        saved = self._save_file_to_disk(product_to_update.id, upload, request)
        print(f'file was saved: {saved}')

        # TODO: do redirect instead of this
        images, indexes = get_files_on_disk(product_to_update.id)

        categories = Product_category.order_by('id', 'asc').get()
        materials = Material.order_by('id', 'asc').get()
        checked_materials = [each.id for each in product_to_update.materials]
        availabilities = Availability.order_by('id', 'asc').get()

        related_products = product_to_update.related_products
        related_products_serialized = add_image_path(related_products.serialize())
        user = self._get_user(request)

        return view.render('admin.edit_product', {
            'product': product_to_update.serialize(),
            'categories': categories.serialize(),
            'materials': materials.serialize(),
            'checked_materials': checked_materials,
            'images': images,
            'related_products': related_products_serialized,
            'user': user,
            'availabilities': availabilities,
        })

        # return [request.input('name'), request.input('description'), request.input('price')]

    def choose_related_products(self, request: Request, view: View):
        all_products = Product.where('id', '<>', request.param('product_id')).order_by('id', 'desc').get()
        caller_product = Product.find(request.param('product_id'))
        serialized_products = add_image_path(all_products.serialize())

        related_products_ids = [related_product.id for related_product in caller_product.related_products]
        user = self._get_user(request)

        # return related_products_ids

        return view.render('admin.choose_related_products', {
            'all_products': serialized_products,
            'caller_product': caller_product,
            'related_products_ids': related_products_ids,
            'user': user,
        })

    def update_related_products(self, request: Request, response: Response):
        product_to_update = Product.find(request.param('product_id'))

        related_product_ids = []
        for each in request.all().keys():
            if each.startswith('prod_'):
                related_product_ids.append(int(each[5:]))

        product_to_update.related_products().sync(related_product_ids)

        # return product_to_update

        return response.redirect('/admin/product/edit/' + str(product_to_update.id))

    def delete_image(self, request: Request, response: Response):
        image_to_delete = request.all()['image_to_delete']
        print(f'  image to delete: {image_to_delete}')

        deleted = self._delete_file(image_to_delete)
        print(f'  image was deleted: {deleted}')

        return response.redirect('/admin/product/edit/' + str(request.all()['caller_id']))

    def save_variant(self, request: Request):
        # print(f' form: {request.all()}')
        variant_id = request.input('variant_id')

        variant = Variant.find(variant_id)
        variant.name = request.input('variant_name')
        variant.price = request.input('variant_price')
        variant.image = request.input('variant_image')
        variant.save()

        return request.redirect(f'/admin/product/edit/{request.input("product_id")}')

    def save_new_variant(self, request: Request):
        product = Product.find(request.input('product_id'))
        print(f' new variant request: {request.all()}')

        price = request.input('variant_price')
        print(f' price: {price}')
        if not price:
            variant = Variant(
                name=request.input('variant_name'),
                image=request.input('variant_image'),
            )
        else:
            variant = Variant(
                name=request.input('variant_name'),
                price=request.input('variant_price'),
                image=request.input('variant_image'),
            )

        variant.product().associate(product)
        variant.save()

        return request.redirect(f'/admin/product/edit/{product.id}')

    def update_cover(self, response: Response):
        categories = Product_category.order_by('id', 'asc').get()

        for category in categories:
            last_product = category.products().order_by('id', 'desc').first()
            try:
                # print(f' last product: {last_product.serialize()}')
                folder_prefix = '/static/img_webp/'
                image_path = folder_prefix + str(last_product.id).zfill(4) + '/' + str(last_product.id).zfill(4) + '_01.webp'
                print(f' cover image path: {image_path}')

                category.image_path = image_path
                category.save()
            except AttributeError:
                pass

        return response.redirect('/')

    def restart_server(self, request: Request, queue: Queue):
        queue.push(RestartWebserverJob, wait="2 seconds")

        return request.redirect('/admin/product/edit')

    def _save_file_to_disk(self, product_id, upload: Upload, request: Request):
        """
        generates folder name and file names
        scans if folder and files exist
        saves file received in request to new file
        :return: True if file was saved
        """
        folder_prefix = 'storage/static/img_webp/'
        folder = folder_prefix + str(product_id).zfill(4)

        product_folder = Path.cwd().joinpath("storage").joinpath("static").joinpath("img_webp").joinpath(str(product_id).zfill(4))
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
            name_to_check = f'{str(product_id).zfill(4)}_{str(counter).zfill(2)}.webp'

            print(f' file {name_to_check} exists: {product_folder.joinpath(name_to_check).exists()}')
            if not product_folder.joinpath(name_to_check).exists():
                file_name_available = True

        if file_name_available:
            try:
                upload.driver('disk').accept('webp').store(request.input("file"), location=folder, filename=name_to_check)
                return True
            except Exception as e:
                print(f' exception during file save: {e}')
                pass

        return False

    def _delete_file(self, image):
        image_name = image.split('/')[-1]
        folder_name = image.split('/')[-2]

        file_to_remove = Path.cwd().joinpath("storage").joinpath("static").joinpath("img_webp").joinpath(folder_name).joinpath(image_name)
        print(f'--- file to remove: {file_to_remove}')

        try:
            remove(str(file_to_remove))
            return True
        except Exception:
            return False

    def _get_user(self, request):
        user = {}
        try:
            user['email'] = request.user().email
            user['role'] = request.user().role.name
        except AttributeError:
            # user = ""
            pass

        return user
