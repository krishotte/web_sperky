import os
import sys

root_path = os.getcwd()
print(f'root path: {root_path}')
sys.path.append(root_path)

from dotenv import load_dotenv

load_dotenv(dotenv_path="F:\\Personal\\prog\\web\\_m_test\\.env", verbose=True)

from app.Material import Material
from app.Product import Product

materials = Material.all()
products = Product.all()

print('existing materials: ')
for each in materials:
    print(f'   {each.serialize()}')

print('existing products: ')
for each in products:
    print(f'   {each.serialize()}')

if products[0].materials.count() == 0:
    products[0].materials().attach(materials[0])
    products[0].materials().attach(materials[1])
    products[1].materials().attach(materials[0])
    products[1].materials().attach(materials[2])
    products[2].materials().attach(materials[0])
    products[2].materials().attach(materials[3])
    products[3].materials().attach(materials[1])
    products[3].materials().attach(materials[4])

for each in products:
    print(f'product: {each.serialize()}')
    for mat in each.materials:
        print(f'    material: {mat.serialize()}')

for each in materials:
    print(f'material: {each.serialize()}')
    for prod in each.products:
        print(f'    product: {prod.serialize()}')
