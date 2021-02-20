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

from app.OrderState import OrderState

if len(OrderState.all()) == 0:
    states = [
        OrderState(
            name='prijatá',
            phase=1,
        ),
        OrderState(
            name='potvrdená',
            phase=2,
        ),
        OrderState(
            name='zaplatená',
            phase=3,
        ),
        OrderState(
            name='odoslaná',
            phase=4,
        ),
        OrderState(
            name='vybavená',
            phase=5,
        ),
        OrderState(
            name='zrušená',
            phase=6,
        ),
    ]

    for state in states:
        state.save()

states_ = OrderState.all()
print(f' order states: {states_.serialize()}')
