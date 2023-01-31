import os


def recreate_folder_tree(folder_tree_file):
    with open(folder_tree_file, "r") as f:
        lines = f.readlines()
    current_folder = ""
    for line in lines:
        print(line)
        line = line.strip()
        if line.endswith("/"):
            current_folder = line
            os.makedirs(current_folder)


recreate_folder_tree("folder_tree.txt")
