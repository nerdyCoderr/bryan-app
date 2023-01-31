import os


def record_folder_tree(folder_path):
    with open("folder_tree.txt", "w") as f:
        for root, dirs, files in os.walk(folder_path):
            f.write(root + "/\n")


record_folder_tree("data")
