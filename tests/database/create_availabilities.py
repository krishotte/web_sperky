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

from app.Availability import Availability

if len(Availability.all()) == 0:
    availabilities = [
        Availability(
            name='Skladom',
            visual_class='btn-outline-success',
        ),
        Availability(
            name='Na objednávku do 3 dní',
            visual_class='btn-outline-warning',
        ),
        Availability(
            name='Na objednávku do 1 týždňa',
            visual_class='btn-outline-warning',
        ),
        Availability(
            name='Na objednávku do 2 týždňov',
            visual_class='btn-outline-warning',
        ),
        Availability(
            name='Vypredané',
            visual_class='btn-outline-danger',
        ),

    ]

    for ava in availabilities:
        ava.save()

availabilities_ = Availability.all()
print(f' availabilities: {availabilities_.serialize()}')
