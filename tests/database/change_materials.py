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

from app.Material import Material

if len(Material.all()) < 6:

    mat_3 = Material.find(3)
    mat_3.name = 'Drôt'

    mat_3.save()

    mat_6 = Material(name='Macrame')
    mat_7 = Material(name='Čipka')

    mat_6.save()
    mat_7.save()

print(f' all materials: {Material.all().serialize()}')



