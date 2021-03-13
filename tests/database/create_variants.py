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

from app.Product import Product
from app.Variant import Variant

product = Product.find(92)
product.load('variants')
print(f' product to modify: {product.serialize()}')

if len(product.variants) == 0:
    var1 = Variant(
        name='variant_1',
        price=12.5,
        image='aa'
    )

    var2 = Variant(
        name='variant_2',
        price=13.3,
        image='bb'
    )

    var1.product().associate(product)
    var1.save()

    var2.product().associate(product)
    var2.save()

product = Product.find(92)
product.load('variants')
print(f' finalized product: {product.serialize()}')


