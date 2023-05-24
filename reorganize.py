import os
import shutil

# set your project root directory
root_dir = "/Users/tachikoma000/Documents/GitHub/ordiView/ordiView"

# create a new 'ordiView' directory inside the current root
new_ordiView_dir = os.path.join(root_dir, "ordiView")
os.makedirs(new_ordiView_dir, exist_ok=True)

# list of files and directories to be moved
items_to_move = ["app", "__init__.py"]

for item in items_to_move:
    source = os.path.join(root_dir, item)
    destination = os.path.join(new_ordiView_dir, item)

    # check if item exists in the source directory
    if os.path.exists(source):
        # move directory or file
        shutil.move(source, destination)
    else:
        print(f"Source not found: {source}")
