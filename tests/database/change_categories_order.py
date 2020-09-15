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

from app.Product_category import Product_category


categories = Product_category.order_by('id', 'asc').get()
print(f'all categories: {categories.serialize()}')

categories[0].name = 'Náušnice_'
categories[1].name = 'Náramky_'
categories[2].name = 'Prívesky_'
categories[3].name = 'Brošne'
categories[4].name = 'Prstene'
categories[5].name = 'Dekorácie'

print(f'all categories: {categories.serialize()}')

categories[0].save()
categories[1].save()
categories[2].save()
categories[3].save()
categories[4].save()
categories[5].save()

categories[0].name = 'Náušnice'
categories[0].image_path = '/static/img/categories/naus.jpg'
categories[1].name = 'Náramky'
categories[1].image_path = '/static/img/categories/nara.jpg'
categories[2].name = 'Náhrdelníky'
categories[2].image_path = '/static/img/categories/priv.jpg'

categories[0].save()
categories[1].save()
categories[2].save()

categories = Product_category.all()
print(f'all categories: {categories.serialize()}')
