import os
import sys

def create_resource_path(resource_path):
    # for root, dirs, files in os.walk(".\\assets", topdown=False):
    #     for file in files:
    #         print(f'{root}\\{file}')
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, resource_path)