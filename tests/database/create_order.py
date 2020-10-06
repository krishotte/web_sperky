import sys
from pathlib import Path

root_path = Path.cwd()
sys.path.append(str(root_path))

from dotenv import load_dotenv
env_path = root_path.joinpath('.env')

load_dotenv(dotenv_path=str(env_path), verbose=True)

from app.User import User
from app.Order import Order

krishotte_user = User.where('email', '=', 'krishotte@seznam.cz').first()
print(f' krishotte user: {krishotte_user.serialize()}')

order1 = Order(shipping_price=2.8, total_price=29)
print(f'  new order: {order1.serialize()}')

# ---------------------------------------
# order1.user().associate(krishotte_user)
# order1.save()

# equivalent to previous:
# krishotte_user.orders().save(order1)

print(f' krishottes orders: {User.where("email", "=", "krishotte@seznam.cz").first().orders.serialize()}')


