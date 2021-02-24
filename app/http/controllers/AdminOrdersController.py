"""A AdminOrdersController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from app.Order import Order
from app.OrderState import OrderState
from app.User import User
from .EditPortfolioController import add_image_path
from .PortfolioController import get_user


class AdminOrdersController(Controller):
    """AdminOrdersController Controller Class."""

    def __init__(self, request: Request):
        """AdminOrdersController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View):
        pass

    def show_all_orders(self, request: Request, view: View):
        """
        all orders
        """
        user = get_user(request)

        orders = Order.order_by('id', 'desc').get()
        orders.load('order_state')
        orders.load('user')

        return view.render('admin/orders/all', {
            'user': user,
            'orders': orders.serialize(),
        })

    def show_one_order(self, request: Request, view: View):
        user = get_user(request)

        order = Order.find(request.param('order_id'))
        order.user
        order.products
        order.order_state
        order.shipping
        order.address

        order_states = OrderState.order_by('id', 'asc').get()

        serialized_products = add_image_path(order.products.serialize())

        return view.render('admin/orders/one', {
            'user': user,
            'order': order.serialize(),
            'order_states': order_states,
            'products': serialized_products,
        })