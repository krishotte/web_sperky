"""A DashboardController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from .PortfolioController import get_user
from .auth.LoginController import get_caller_path
from app.Product import Product
from app.Order import Order


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
        # print(f' environ: {request.environ}')
        print(f' caller: {request.header("HTTP_REFERER")}')

        print(f' session: {request.session.all()}')

        return view.render('dash/profile', {
            'user': user,
        })

    def show_orders(self, request: Request, view: View):
        user = get_user(request)
        return view.render('dash/orders', {
            'user': user,
        })

    def show_cart(self, request: Request, view: View):
        user = get_user(request)

        items = request.session.get('ordered_items')
        unique_items = list(set(items))
        counts = [items.count(item) for item in unique_items]
        print(f' unique items: {unique_items}')
        print(f' counts: {counts}')

        total_price = 0
        products = []
        for index, each in enumerate(unique_items):
            product = Product.find(each)
            products.append(product.serialize())
            total_price += product.price * counts[index]
        print(f' total price: {total_price}')

        request.session.set('unique_items', unique_items)
        request.session.set('counts', counts)
        request.session.set('total_price', total_price)
        # print(f' products: {products}')
        return view.render('dash/cart', {
            'user': user,
            'ordered_items': unique_items,
            'counts': counts,
            'products': products,
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
