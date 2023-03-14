import random
from pathlib import Path

import jsonlines as jsonl
import numpy as np
from tqdm import tqdm
from typing import Tuple

from macarons.image_text import generate_datapoint
from skimage.io import imsave

TASKS = ['all', 'image_caption', 'visual_question_answer']


def build(
    output_dir: Path,
    image_size: Tuple[int, int] = (224, 224),
    amount: int = 1000,
    task: str = 'all',
    seed: int = 42,
):
    """Build dataset

    Available tasks: all, image caption, visual question answer

    Parameters
    ----------
    output_dir : Path
        where the dataset directory should be contained
    image_size : Tuple[int, int], optional
        height, width, by default (224, 224)
    amount : int, optional
        number of samples, by default 1000
    task : str, optional
        dataset type, by default 'all'
    seed : int, optional
        random seed, by default 42

    Raises
    ------
    ValueError
        When unknown task is specified
    """
    if task not in TASKS:
        raise ValueError(f'Unknown task. Task should be in {TASKS}')
    random.seed(seed)
    np.random.seed(seed)

    image_path = output_dir.joinpath(f'macarons-{task}/image')
    image_path.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir.joinpath(f'macarons-{task}/map.jsonl')

    with jsonl.open(jsonl_path, 'w') as fp:
        for i in tqdm(range(amount)):
            dp = generate_datapoint(*image_size)

            if task in ['all', 'image_caption']:
                dp.make_caption()

            if task in ['all', 'visual_question_answer']:
                dp.make_question_answer_list()

            image_id = str(i).zfill(6)
            dp.make_id_path(image_id, Path(f'image/{image_id}.jpg'))  # relative to map.jsonl
            imsave(
                image_path.joinpath(f'{image_id}.jpg'),  # relative to image_path and output_dir
                dp.image,
                check_contrast=False,
            )

            if task == 'image_caption':
                fp.write(dp.to_dict(exclude=('image', 'question_answer_list')))

            if task == 'visual_question_answer':
                fp.write(dp.to_dict(exclude=('image', 'caption')))

            if task == 'all':
                fp.write(dp.to_dict(exclude=('image')))


if __name__ == '__main__':
    for task in TASKS:
        build(Path('demo_data'), amount=10, task=task)
