import os
import sys

from dotenv import load_dotenv

print(f'current path: {os.path.realpath(__file__)}')
"""
root_path = os.path.split(os.path.split(os.getcwd())[0])[0]
print(f'root path: {root_path}')
sys.path.append(root_path)
"""

root_path = os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], ".env")
print(f'  {os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], ".env")}')

# load_dotenv(dotenv_path=root_path, verbose=True)

load_dotenv(dotenv_path="F:\\Personal\\prog\\web\\_m_test\\.env", verbose=True)

from app.Product_category import Product_category


categories = Product_category.all()

print('existing categories: ')
for each in categories:
    print(f'   {each.id}, {each.name}')
    
if len(categories) == 0:
    new_cats = [
        Product_category(name='Prívesky'),
        Product_category(name='Náušnice'),
        Product_category(name='Náramky'),
        Product_category(name='Brošne'),
        Product_category(name='Prstene'),
        Product_category(name='Dekorácie'),
    ]

    for each in new_cats:
        each.save()

