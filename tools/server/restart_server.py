import subprocess
import sys
from masonite import env


"""
from pathlib import Path
from dotenv import load_dotenv


root_path = Path.cwd()
env_path = root_path.joinpath('.env')
print(f'  root path: {root_path}')
print(f'  env path: {env_path}')

sys.path.append(str(root_path))
load_dotenv(dotenv_path=env_path, verbose=True)
"""

server_1 = env("WEB_SERVER_SERVICE_1")
print(f' server1: {server_1}')
server_2 = env("WEB_SERVER_SERVICE_2")
print(f' server2: {server_2}')


def restart_server():
    if len(server_1) > 0:
        subprocess.run(['sudo', 'systemctl', 'restart', server_1])

    if len(server_2) > 0:
        subprocess.run(['sudo', 'systemctl', 'restart', server_2])
