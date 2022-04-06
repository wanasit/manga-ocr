import glob
import os
import json
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Union

from PIL import Image

from manga_ocr.utils.nb_annotation import find_annotation_data_for_image

current_module_dir = os.path.dirname(__file__)
project_root_dir = os.path.join(current_module_dir, '../../')

PathLike = Union[
    Path,
    str
]


def get_path_project_dir(child='') -> str:
    path = os.path.join(project_root_dir, child)
    return path


def get_path_example_dir(child='') -> str:
    path = get_path_project_dir('example')
    path = os.path.join(path, child)
    return path


def load_images_with_annotation(
        glob_file_pattern: PathLike,
        alt_annotation_directory: Optional[PathLike] = None
) -> Tuple[List[Image.Image], List[Optional[Dict]]]:
    files = glob.glob(str(glob_file_pattern))
    images = []
    annotations = []
    for file in sorted(files):
        images.append(load_image(file))

        annotation_file = find_annotation_data_for_image(file, alt_annotation_directory)
        annotations.append(annotation_file)

    return images, annotations


def load_images(glob_file_pattern: PathLike) -> List[Image.Image]:
    files = glob.glob(str(glob_file_pattern))
    images = []
    for file in sorted(files):
        images.append(load_image(file))

    return images


def load_image(file: PathLike) -> Image.Image:
    with Image.open(file) as img:
        return img.copy()


def load_texts(text_file: PathLike):
    with open(text_file) as f:
        return [line.strip() for line in f.readlines()]


def load_json_dict(json_file: PathLike) -> Dict:
    with open(json_file) as f:
        return json.load(f)


def write_json_dict(json_file: PathLike, data: Dict):
    with open(json_file, 'w') as f:
        return json.dump(data, f)
