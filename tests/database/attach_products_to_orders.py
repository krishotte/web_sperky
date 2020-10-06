import sys
from pathlib import Path

root_path = Path.cwd()
sys.path.append(str(root_path))

from dotenv import load_dotenv
env_path = root_path.joinpath('.env')

load_dotenv(dotenv_path=str(env_path), verbose=True)

from app.Order import Order
from app.Product import Product

order1 = Order.find(1)
print(f' order: {order1.serialize()}')

product1 = Product.find(2)
product2 = Product.find(3)
product3 = Product.find(6)

# order1.products().attach(product1, {'product_count': 1, 'unit_price': 13.2})
order1.products().attach(product2, {'product_count': 2, 'unit_price': 14.2})
order1.products().attach(product3, {'product_count': 3, 'unit_price': 15.2})


