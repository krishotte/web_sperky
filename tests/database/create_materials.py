import os
import sys

root_path = os.getcwd()
print(f'root path: {root_path}')
sys.path.append(root_path)

from dotenv import load_dotenv

load_dotenv(dotenv_path="F:\\Personal\\prog\\web\\_m_test\\.env", verbose=True)

from app.Material import Material

materials = Material.all()

print('existing materials: ')
for each in materials:
    print(f'   {each.serialize()}')

if len(materials) == 0:
    new_products = [
        Material(name='Živica'),
        Material(name='Drevo'),
        Material(name='Čipka'),
        Material(name='Polymér'),
        Material(name='Koráliky'),
        Material(name='Strapce'),
    ]

    for each in new_products:
        each.save()
