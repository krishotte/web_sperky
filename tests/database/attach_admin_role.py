import sys
from pathlib import Path

root_path = Path.cwd()
sys.path.append(str(root_path))

from dotenv import load_dotenv
env_path = root_path.joinpath('.env')

load_dotenv(dotenv_path=str(env_path), verbose=True)

from app.Role import Role
from app.User import User

admin_role = Role.where('name', '=', 'admin').first()
print(f' admin role: {admin_role.serialize()}')

krishotte_user = User.where('email', '=', 'krishotte@seznam.cz').first()
print(f' krishotte user: {krishotte_user.serialize()}')

if krishotte_user.role_id is None:
    print(f' attaching admin role to {krishotte_user.email}')
    krishotte_user.role().associate(admin_role)
    krishotte_user.save()

    krishotte_user = User.where('name', '=', 'krishotte').first()
    print(f' krishotte user: {krishotte_user.serialize()}')
