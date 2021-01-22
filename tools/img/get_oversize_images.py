from pathlib import Path
from PIL import Image

root_path = Path.cwd().parent.parent
print(f' root path: {root_path}')

img_folder = root_path.joinpath('storage').joinpath('static').joinpath('img')
print(f' img folder: {img_folder}')

product_folders = [folder for folder in img_folder.iterdir()]
# print(f' product folders: {product_folders}')

img_files = [file for file in product_folders[0].iterdir()]
# print(f' img files: {img_files}')

for folder in product_folders:
    if folder.is_dir():
        # print(f' product folder: {folder}')
        img_files = [file for file in folder.iterdir()]

        for file in img_files:
            # print(f'   img file: {file}')
            with Image.open(str(file)) as image:
                # print(f'    size: {image.size}')
                image_size = image.size

            if image_size[0] != 700:
                print(f'   img file: {file}, size: {image_size}')

