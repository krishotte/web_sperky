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
from app.Shipping import Shipping
from app.OrderState import OrderState
from masonite import env
import pendulum


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
        user_ = User.where('email', '=', user['email']).first()
        user_.addresses()

        return view.render('dash/profile', {
            'user': user,
            'user_': user_,
        })

    def show_profile(self, request: Request, view: View):
        user = get_user(request)
        user_ = User.where('email', '=', user['email']).first()
        user_.addresses()

        if user_.verified_at is not None:
            print(f' user verified')
        # print(f' environ: {request.environ}')
        print(f' APP_URL: {request.header("APP_URL")}')
        # print(f' env: {env("APP_URL")}')

        return view.render('dash/profile', {
            'user': user,
            'user_': user_,
        })

    def show_orders(self, request: Request, view: View):
        user = get_user(request)

        orders = request.user().orders().order_by('id', 'desc').get()
        orders.load('order_state')

        for order in orders:
            print(f' datetime: {order.created_at.strftime("%Y-%m-%d")}')

        print(f' your orders: {orders.serialize()}')

        return view.render('dash/orders', {
            'user': user,
            'orders': orders.serialize(),
        })

    def show_single_order(self, request: Request, view: View):
        user = get_user(request)
        order = Order.find(request.param('order_id'))
        order.address
        order.shipping
        order.order_state
        print(f' order to display: {order.serialize()}')

        serialized_products = add_image_path(order.products.serialize())
        print(f' products: {order.products.serialize()}')

        if order.user.email == user['email']:
            return view.render('dash/single_order', {
                'user': user,
                'order': order.serialize(),
                'products': serialized_products,
            })
        else:
            print(f' not your order')
            return request.redirect('/dashboard/orders')

    # cart control methods
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
        """
        items to order are held in cookie as list
        items can be in list multiple times
        """
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

    def remove_from_cart(self, request: Request, view: View):
        """
        remove one item from cart
        """
        caller = get_caller_path(request)

        item_to_remove = int(request.input('item_to_remove'))
        ordered_items = request.session.get('ordered_items')
        print(f' ordered items before del: {ordered_items}')

        index_of_item = ordered_items.index(item_to_remove)
        ordered_items.pop(index_of_item)
        print(f' ordered items after del: {ordered_items}')

        request.session.set('ordered_items', ordered_items)
        return request.redirect(caller)

    # order control methods
    def order_show_user_details(self, request: Request, view: View):
        """
        first step of order
        user select address to send order to
        """
        user = get_user(request)
        user_ = User.where('email', '=', user['email']).first()
        user_.addresses()

        print(f' user addresses: {user_.addresses.serialize()}')

        return view.render('dash/order/user_data', {
            'user': user,
            'user_': user_,
        })

    def order_set_user_address(self, request: Request):
        """
        sets order address to cookie
        redirects to shipping
        """
        address_id = int(request.input('address_id'))
        address = Address.find(address_id)
        print(f' address to use: {address.serialize()}')

        request.session.set('address', address.id)

        return request.redirect('/order-shipping')

    def order_show_shipping(self, request: Request, view: View):
        """
        allows to go back from order review
        """
        user = get_user(request)
        user_ = User.where('email', '=', user['email']).first()
        user_.addresses()

        shippings = Shipping.all()

        return view.render('dash/order/shipping', {
            'user': user,
            'user_': user_,
            'shippings': shippings,
        })

    def order_set_shipping(self, request: Request):
        """
        saves shipping to session, redirects to order review
        """
        request.session.set('shipping', int(request.input('shipping_id')))

        return request.redirect('/order-review')

    def order_back_to_shipping(self, request: Request):
        """
        saves note to session, redirects to order_show_shipping
        """
        note = request.input('note')
        print(f' saving note to session: {note}')
        request.session.set('note', note)

        return request.redirect('/order-shipping')

    def order_review(self, request: Request, view: View):
        """
        shows order review
        """
        user = get_user(request)
        user_ = User.where('email', '=', user['email']).first()

        shipping = Shipping.find(int(request.session.get('shipping')))
        address = Address.find(int(request.session.get('address')))

        items = request.session.get('ordered_items')
        unique_items = list(set(items))
        counts = [items.count(item) for item in unique_items]

        note = request.session.get('note')

        total_price = shipping.price
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

        request.session.set('total_price', total_price)

        return view.render('dash/order/review_order', {
            'user': user,
            'user_': user,
            'ordered_items': unique_items,
            'counts': counts,
            'products': serialized_products,
            'total_price': total_price,
            'shipping': shipping,
            'address': address,
            'note': note,
        })

    def make_order(self, request: Request):
        print(f' session: {request.session.all()}')

        shipping = Shipping.find(int(request.session.get('shipping')))
        address = Address.find(int(request.session.get('address')))

        items = request.session.get('ordered_items')
        unique_items = list(set(items))
        counts = [items.count(item) for item in unique_items]

        note = request.input('note')
        total_price = float(request.session.get('total_price'))
        products = []
        try:
            for index, each in enumerate(unique_items):
                product = Product.find(each)
                products.append(product)
        except Exception:
            pass

        # let's make an order
        order = Order(total_price=total_price, note=note)
        order.user().associate(request.user())

        order_state = OrderState.where('phase', '=', 1).first()
        order.order_state().associate(order_state)

        order.shipping().associate(shipping)
        order.address().associate(address)

        # save to get an id
        order.save()

        order.name = f"{pendulum.now().format('%Y')}{str(order.id).zfill(4)}"
        order.save()

        for index, product in enumerate(products):
            order.products().attach(product, {
                'product_count': counts[index],
                'unit_price': product.price,
            })

        # clear session
        request.session.reset()

        return request.redirect('/dashboard/orders')

    # user address control methods
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
