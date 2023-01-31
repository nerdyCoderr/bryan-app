import os
import shutil

data_folder = 'data/'

for root, dirs, files in os.walk(data_folder):
    for file in files:
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
            except Exception as e:
                print("Error deleting file:", file_path)
                print(e)
