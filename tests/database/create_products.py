import os
import sys

root_path = os.getcwd()
print(f'root path: {root_path}')
sys.path.append(root_path)

from dotenv import load_dotenv

load_dotenv(dotenv_path="F:\\Personal\\prog\\web\\_m_test\\.env", verbose=True)

from app.Product import Product
from app.Product_category import Product_category

products = Product.all()
categories = Product_category.all()

print('existing categories: ')
for each in categories:
    print(f'   {each.serialize()}')


if len(products) == 0:
    new_products = [
        Product(name='Aaaéé', category_id=1, price=12.3),
        Product(name='Bbaíí', category_id=2, price=13.3),
        Product(name='Feúú', category_id=3, price=14.3),
        Product(name='Lúaf', category_id=1, price=15.3),
        Product(name='Pardf', category_id=2, price=16.3),
        Product(name='Dfark', category_id=2, price=17.3),
    ]

    for each in new_products:
        each.save()

print('products: ')
for each in products:
    print(f'   {each.id}, {each.name}, {each.category_id}')

# products_1 = Product.has('category_id', '==', 2).get()
products_1 = Product_category.find(2).products
print(f'category 2, products: {len(products_1)}')
for each in products_1:
    print(f'  {each.serialize()}')

not_empty_categories = Product_category.has('products').get()
print(f'not empty categories:')
for each in not_empty_categories:
    print(f'  {each.serialize()}')

categories_1 = Product_category.all()
for each in categories_1:
    print(f'category: {each.serialize()}')
    for prod in each.products:
        print(f'    product: {prod.serialize()}')