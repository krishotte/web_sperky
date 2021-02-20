import sys
from pathlib import Path

root_path = Path.cwd()
sys.path.append(str(root_path))

from dotenv import load_dotenv
env_path = root_path.joinpath('.env')

load_dotenv(dotenv_path=str(env_path), verbose=True)

from app.User import User
from app.Order import Order
from app.Product import Product
from app.Shipping import Shipping
from app.OrderState import OrderState

krishotte_user = User.where('email', '=', 'krishotte@seznam.cz').first()
print(f' krishotte user: {krishotte_user.serialize()}')

krishotte_user.addresses

items = [
    Product.find(1),
    Product.find(3),
    Product.find(5),
]
print(f' items to order: {[item.serialize() for item in items]}')

shipping = Shipping.find(2)

price = sum([product.price for product in items]) + shipping.price
print(f' total price: {price}')

order_state = OrderState.where('phase', '=', 1).first()
print(f' order state: {order_state.serialize()}')

order1 = Order(total_price=price)
print(f'  new order: {order1.serialize()}')

# ---------------------------------------
order1.user().associate(krishotte_user)
# order1.save()

# equivalent to previous:
# krishotte_user.orders().save(order1)

order1.order_state().associate(order_state)
# order1.save()
print(f' order after state attach: {order1.serialize()}')

order1.shipping().associate(shipping)
order1.address().associate(krishotte_user.addresses[0])
# save possible only if all belongs_to are set
order1.save()

# attach products with pivot data
for item in items:
    order1.products().attach(item, {
        'product_count': 1,
        'unit_price': item.price
    })

print(f' order after products add: {order1.serialize()}')

# print(f' krishottes orders: {User.where("email", "=", "krishotte@seznam.cz").first().orders.serialize()}')


