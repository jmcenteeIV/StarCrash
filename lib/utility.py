import os
import sys


def create_resource_path(resource_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        print("MEIPASS: " + str(sys._MEIPASS))
        base_path = sys._MEIPASS
    except Exception:
        print ("No MEIPASS")
        base_path = os.path.abspath(".")

    return os.path.join(base_path, resource_path)