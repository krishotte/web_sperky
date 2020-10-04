import sys
from pathlib import Path

root_path = Path.cwd()
sys.path.append(str(root_path))

from dotenv import load_dotenv
env_path = root_path.joinpath('.env')

load_dotenv(dotenv_path=str(env_path), verbose=True)

from app.Role import Role

roles_count = Role.count()
print(f' roles: {roles_count}')

if roles_count == 0:
    role = Role(name='admin')
    role.save()

roles = Role.all()
print(f' all roles: {roles.serialize()}')
