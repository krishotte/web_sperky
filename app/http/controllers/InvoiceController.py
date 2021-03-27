"""A InvoiceController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from app.http.controllers.auth.LoginController import get_caller_path
from app.Invoice import Invoice
from app.Order import Order
from app.Variant import Variant
from orator.exceptions.orm import ModelNotFound
import pendulum
from app.tools.invoice import create as create_invoice
from pathlib import Path
from masonite.response import Download


class InvoiceController(Controller):
    """InvoiceController Controller Class."""

    def __init__(self, request: Request):
        """InvoiceController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, request: Request, view: View):
        invoice_id = request.param('invoice_id')
        invoice = Invoice.find(invoice_id)

        file_name = str(get_invoice_path(invoice))
        return Download(file_name)

    def create_invoice(self, request: Request):
        caller = get_caller_path(request)
        order_id = request.input('order_id')
        print(f' creating invoice for order id: {order_id}')

        order = Order.find(order_id)
        order.address
        order.shipping

        products = order.products
        for product in products:
            if product.pivot.variant_id:
                product.load({
                    'variants': Variant.query().where('id', '=', product.pivot.variant_id)
                })

        number = get_new_invoice_number()
        prefix = ''
        year = pendulum.now().format("%Y")
        variable_symbol = f'00{year}{str(number).zfill(4)}'
        issue_date = pendulum.now()
        due_date = issue_date.add(days=14)

        invoice = Invoice(
            prefix='',
            year=year,
            number=number,
            variable_symbol=variable_symbol,
            issue_date=issue_date,
            due_date=due_date,
        )
        print(f' new invoice: {invoice.serialize()}')

        invoice.order().associate(order)
        invoice.save()

        order.invoice

        file_name = str(get_invoice_path(invoice))
        create_invoice(order.serialize(), products.serialize(), file_name)

        return request.redirect(caller)


def get_new_invoice_number(prefix='', year=2021):
    try:
        invoices = Invoice.where('prefix', '=', prefix).where('year', '=', year).order_by('number', 'desc').first_or_fail()
        new_number = invoices.number + 1
        print(f' last invoice: {invoices.serialize()}')
    except ModelNotFound:
        new_number = 1

    print(f' new invoice number: {new_number}')

    return new_number


def get_invoice_path(invoice: Invoice) -> Path:
    file_name = invoice.variable_symbol

    root_path = Path.cwd()
    invoice_dir = root_path.joinpath('storage').joinpath('invoice').joinpath(str(invoice.year))
    if not invoice_dir.exists():
        print(f' creating dir: {invoice_dir}')
        invoice_dir.mkdir()

    invoice_file_path = invoice_dir.joinpath(f'{file_name}.pdf')
    print(f' invoice file: {invoice_file_path}')

    return invoice_file_path
