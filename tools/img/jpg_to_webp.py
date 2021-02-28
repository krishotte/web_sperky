from PIL import Image
from pathlib import Path
from typing import List
import copy


root_dir = Path.cwd()
static_dir = root_dir.joinpath('storage').joinpath('static')

test_static_dir = Path('f:\\Personal\\prog\\web\\_pieskovisko\\image_manipulation')


def process_dir(dir_: Path, webp_dir: Path, subdirs: list):
    subdirs_main = copy.deepcopy(subdirs)  # need to use deepcopy otherwise original list gets overwritten
    print(f' subdirs: {subdirs_main}')
    items = dir_.iterdir()

    print(f' {dir_} contains directories:')
    for item in items:
        subdirs_ = copy.deepcopy(subdirs)
        if item.is_dir():
            print(f'   dir: {item.name}')
            subdirs_.append(item.name)
            process_dir(item, webp_dir, subdirs_)  # recursively run again on subdir

    print(f' {dir_} contains jpeg files:')
    for jpg_file in dir_.glob('*.jpg'):
        print(f'   jpeg: {jpg_file.name}')

        image = Image.open(str(jpg_file))
        image_out = image.convert('RGB')

        webp_file = webp_dir
        if not webp_file.exists():
            webp_file.mkdir()

        # build new_file path and create not existing subdirs
        for subdir in subdirs_main:
            webp_file = webp_file.joinpath(subdir)
            if not webp_file.exists():
                webp_file.mkdir()

        new_file = f'{jpg_file.stem}.webp'
        webp_file = webp_file.joinpath(new_file)
        print(f'    about to write file: {webp_file}')
        image_out.save(str(webp_dir.joinpath(webp_file)), 'webp', method=6)

        image.close()
        image_out.close()


def main(static_dir_=static_dir, input_dir='img', output_dir='img_webp'):
    print(f' your static dir: {static_dir_}')
    jpg_dir = static_dir_.joinpath(input_dir)
    webp_dir = static_dir_.joinpath(output_dir)
    process_dir(jpg_dir, webp_dir, [])


if __name__ == '__main__':
    main()
