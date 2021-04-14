# to be run from main directory
import sys
from pathlib import Path
from dotenv import load_dotenv
import os


root_path = Path.cwd()
env_path = root_path.joinpath('.env')
print(f'  root path: {root_path}')
print(f'  env path: {env_path}')

sys.path.append(str(root_path))
load_dotenv(dotenv_path=env_path, verbose=True)
# print(f' env: {os.environ}')

from app.tools.sitemap import Sitemap
from app.Product import Product

sm = Sitemap(changefreq='weekly', sitemap_url='https://sperkyodvierky.sk/')

sm.add('https://sperkyodvierky.sk/portfolio')

sm.add('https://sperkyodvierky.sk/blog/1', priority=0.5, lastmod='today')

products = Product.order_by('id', 'asc').get()
# print(f' all products: {products.serialize()}')

for product in products:
    sm.add(f'https://sperkyodvierky.sk/product/{product.id}',
           changefreq='weekly',
           priority=0.7,
           lastmod='today')

print(f' xml: {repr(sm)}')

sitemap_file = root_path.joinpath('storage').joinpath('sitemap_test.xml')
print(f' writing file: {str(sitemap_file)}')

sm.write(str(sitemap_file))
