import os

import os.path
from os import path

def delete_files():

    my_path = "C:\\Users\\HP6125047\\AppData\\Local\\Programs\\Python\\Python39\\Scripts\\General Test3.2\\Tests\\V32 Tests"
    for root, dirs, files in os.walk(my_path):
        for file in files:
            os.remove(os.path.join(root,file))

delete_files()
