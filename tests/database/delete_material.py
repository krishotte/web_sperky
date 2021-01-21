# to be run from root directory
# material must not be referenced to be deleted

import sys
from pathlib import Path

root_path = Path.cwd()
sys.path.append(str(root_path))

from dotenv import load_dotenv
env_path = root_path.joinpath('.env')

load_dotenv(dotenv_path=str(env_path), verbose=True)

from app.Material import Material
from app.Product import Product

print(f' all materials: {Material.all().serialize()}')

# material to delete
# material_to_delete = Material.find(4)
try:
    material_to_delete = Material.where('name', '=', 'Polymér').get()[0]
    print(f' material to delete: {material_to_delete.serialize()}')
    material_to_delete.delete()
except IndexError:
    print(f' material not found')
