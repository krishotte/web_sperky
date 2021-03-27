# to be run from main directory
import sys
from pathlib import Path
from dotenv import load_dotenv


root_path = Path.cwd()
env_path = root_path.joinpath('.env')
print(f'  root path: {root_path}')
print(f'  env path: {env_path}')

sys.path.append(str(root_path))
load_dotenv(dotenv_path=env_path, verbose=True)

from app.tools import invoice
from app.Order import Order
from app.Variant import Variant

order = Order.find(29)
order.address
order.shipping
order.invoice

products = order.products
for product in products:
    if product.pivot.variant_id:
        product.load({
            'variants': Variant.query().where('id', '=', product.pivot.variant_id)
        })

print(f' order to process: {order.serialize()}')

var_symbol = str(int(order.name)).zfill(10)
print(f' variabilny symbol: {var_symbol}')

serialized_order = order.serialize()
# serialized_order['order_date'] = order.created_at.format("%d.%m.%Y")
# serialized_order['due_date'] = order.created_at.add(days=14).format("%d.%m.%Y")
# serialized_order['var_symbol'] = var_symbol

print(f' ordered products: {products.serialize()}')

print(f' order: {serialized_order}')

root_path = Path().cwd()
invoice_file = root_path.joinpath('storage').joinpath('invoice').joinpath('test').joinpath('faktura01.pdf')
print(f' root path: {root_path}')
print(f' invoice path: {invoice_file}')

invoice.create(serialized_order, products.serialize(), invoice_file)
