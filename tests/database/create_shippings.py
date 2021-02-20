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

from app.Shipping import Shipping

if len(Shipping.all()) == 0:
    shippings = [
        Shipping(
            name='osobný odber',
            price=0,
        ),
        Shipping(
            name='poštou',
            price=2,
        )
    ]

    for shipping in shippings:
        shipping.save()

shippings = Shipping.all()
print(f' shippings: {shippings.serialize()}')