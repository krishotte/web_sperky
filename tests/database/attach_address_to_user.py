import sys
from pathlib import Path

root_path = Path.cwd()
sys.path.append(str(root_path))

from dotenv import load_dotenv
env_path = root_path.joinpath('.env')

load_dotenv(dotenv_path=str(env_path), verbose=True)

from app.User import User
from app.Address import Address

krishotte_user = User.where('email', '=', 'krishotte@seznam.cz').first()
print(f' krishotte user: {krishotte_user.serialize()}')

address1 = Address(
    street='Sancova 8',
    zip_code='900 11',
    city='Bratislava',
    name='Peter Krššák',
    phone='+421905104500',
)
# print(f' address to attach: {address1.serialize()}')

# krishotte_user.addresses().save(address1)

print(f' krishotte has addresses: {krishotte_user.addresses.count()}')
print(f'   addresses: {krishotte_user.addresses.serialize()}')
