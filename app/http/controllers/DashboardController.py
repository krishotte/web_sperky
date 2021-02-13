"""A DashboardController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from .PortfolioController import get_user
from .auth.LoginController import get_caller_path
from app.Product import Product
from app.Order import Order
from .EditPortfolioController import add_image_path
from app.User import User
from app.Address import Address


class DashboardController(Controller):
    """DashboardController Controller Class."""

    def __init__(self, request: Request):
        """DashboardController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, request: Request, view: View):
        user = get_user(request)

        return view.render('dash/menu', {
            'user': user,
        })

    def show_profile(self, request: Request, view: View):
        user = get_user(request)
        user_ = User.where('email', '=', user['email']).get()[0]
        user_.addresses()
        # print(f' environ: {request.environ}')
        print(f' caller: {request.header("HTTP_REFERER")}')

        print(f' session: {request.session.all()}')

        return view.render('dash/profile', {
            'user': user,
            'user_': user_,
        })

    def show_orders(self, request: Request, view: View):
        user = get_user(request)

        orders = request.user().orders

        print(f' your orders: {orders.serialize()}')

        return view.render('dash/orders', {
            'user': user,
            'orders': orders.serialize(),
        })

    def show_single_order(self, request: Request, view: View):
        user = get_user(request)
        order = Order.find(request.param('order_id'))

        serialized_products = add_image_path(order.products.serialize())
        print(f' products: {order.products.serialize()}')

        return view.render('dash/single_order', {
            'user': user,
            'order': order.serialize(),
            'products': serialized_products,
        })

    def show_cart(self, request: Request, view: View):
        user = get_user(request)

        try:
            items = request.session.get('ordered_items')
            unique_items = list(set(items))
            counts = [items.count(item) for item in unique_items]
            print(f' unique items: {unique_items}')
            print(f' counts: {counts}')
        except Exception:
            counts = 0
            unique_items = []

        total_price = 0
        products = []
        try:
            for index, each in enumerate(unique_items):
                product = Product.find(each)
                products.append(product.serialize())
                total_price += product.price * counts[index]
            print(f' total price: {total_price}')
            serialized_products = add_image_path(products)
        except Exception:
            serialized_products = []

        request.session.set('unique_items', unique_items)
        request.session.set('counts', counts)
        request.session.set('total_price', total_price)
        # print(f' products: {products}')
        return view.render('dash/cart', {
            'user': user,
            'ordered_items': unique_items,
            'counts': counts,
            'products': serialized_products,
            'total_price': total_price,
        })

    def add_to_cart(self, request: Request):
        caller = get_caller_path(request)
        # request.session.reset()

        if request.session.has('ordered_items'):
            items = request.session.get('ordered_items')
            items.append(int(request.param('product_id')))
            request.session.set('ordered_items', items)
        else:
            request.session.set('ordered_items', [int(request.param('product_id'))])

        print(f' session : {request.session.all()}')
        return request.redirect(caller)

    def make_order(self, request: Request):
        print(f' session: {request.session.all()}')

        order = Order(shipping_price=0, total_price=float(request.session.get('total_price')))
        print(f' order: {order.serialize()}')

        order.user().associate(request.user())
        order.save()

        for index, product in enumerate(request.session.get('unique_items')):
            order.products().attach(product, {
                'product_count': request.session.get('counts')[index],
                'unit_price': Product.find(product).price
            })

        return request.redirect('/dashboard/orders')

    def show_new_address(self, request: Request, view: View):
        """
        shows form for new user address
        """
        user = get_user(request)
        print(f' logged in user: {user}')
        return view.render('dash/new_address', {
            'user': user,
        })

    def store_new_address(self, request: Request):
        user = get_user(request)
        print(f' logged in user: {user}')
        
        user_ = User.where('email', '=', user['email']).first_or_fail()

        address1 = Address(
            street=request.input('street'),
            zip_code=request.input('zip_code'),
            city=request.input('city'),
            name=request.input('name'),
            phone=request.input('phone'),
        )
        print(f' address to store: {address1}')

        user_.addresses().save(address1)

        return request.redirect('/dashboard/profile')

    def show_existing_address(self, request: Request, view: View):
        user = get_user(request)
        print(f' logged in user: {user}')

        address_id = request.param('address_id')
        address_ = Address.find(address_id)

        if address_.user.email == user['email']:
            print(f' your address')
            # return request.redirect('/dashboard/profile')
            return view.render('dash/existing_address', {
                'user': user,
                'address': address_,
            })
        else:
            print(f' not your address')
            return request.redirect('/dashboard')

    def store_existing_address(self, request: Request):
        user = get_user(request)
        print(f' logged in user: {user}')

        user_ = User.where('email', '=', user['email']).first_or_fail()

        address1 = Address.find(request.input('id'))
        address1.street = request.input('street')
        address1.zip_code = request.input('zip_code')
        address1.city = request.input('city')
        address1.name = request.input('name')
        address1.phone = request.input('phone')

        print(f' address to store: {address1.serialize()}')

        address1.save()

        return request.redirect('/dashboard/profile')

    def delete_address(self, request: Request):
        user = get_user(request)
        print(f' logged in user: {user}')

        address_id = request.param('address_id')
        address_ = Address.find(address_id)

        if address_.user.email == user['email']:
            print(f' your address, deleting ...')
            # return request.redirect('/dashboard/profile')
            address_.delete()

            return request.redirect('/dashboard/profile')

        else:
            print(f' not your address')
            return request.redirect('/dashboard')
