from pathlib import Path


def upload_image(filename: str, blob: bytes) -> bool:
    path_to_static = '../static/movies/images/'

    if Path(f'{path_to_static}{filename}').is_file():
        return False
    else:
        with open(f'{path_to_static}{filename}', 'wb') as file:
            file.write(blob)
            return True


def update_images(images: dict) -> None:
    path_to_static = '../static/movies/images/'

    for filename in images.keys():
        if Path(f'{path_to_static}{filename}').is_file():
            pass
        else:
            with open(f'{path_to_static}{filename}', 'wb') as file:
                file.write(images[filename])
