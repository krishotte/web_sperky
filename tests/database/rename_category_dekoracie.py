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

print(f' categories: {Product_category.all().serialize()}')

try:
    dek_ = Product_category.where('name', '=', 'Dekorácie').first()
    dek_.name = 'Ostatné'
    dek_.save()

    print(f' dek_: {dek_.serialize()}')
except AttributeError:
    print(f' category dekoracie does not exist')


