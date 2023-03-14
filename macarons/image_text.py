import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
import json

import numpy as np
from webcolors import CSS3_NAMES_TO_HEX, hex_to_rgb
from skimage.draw import disk
from skimage.io import imsave
from dataclass_wizard import JSONWizard
from dataclass_wizard.enums import LetterCase


@dataclass
class Datapoint(JSONWizard):
    class _(JSONWizard.Meta):
        # Sets the target key transform to use for serialization;
        # defaults to `camelCase` if not specified.
        key_transform_with_load = LetterCase.SNAKE
        key_transform_with_dump = LetterCase.SNAKE

    image: np.ndarray
    circle_color_name: str
    background_color_name: str

    caption: str = ""
    question_answer_list: List[List[str]] = field(default_factory=list)
    image_id: str = ""
    image_path: str = ""

    def make_caption(self):
        """Make attributes: caption

        The format: f'The {self.circle_color_name} circle on the {self.background_color_name} background'
        """
        self.caption = f'The {self.circle_color_name} circle on the {self.background_color_name} background'

    def make_question_answer_list(self):
        """Make attributes: question_answer_list

        A list of question and answer
        """
        self.question_answer_list = [
            ['What is the color of the circle', self.circle_color_name],
            ['What is the color of the background', self.background_color_name],
            [
                'What are the color of the circle and the background',
                f'{self.circle_color_name} and {self.background_color_name}',
            ],
        ]

    def make_id_path(self, image_id: str, path: Path):
        """Make attributes: image_id, image_path

        Parameters
        ----------
        image_id : str
            6 digits e.g 000420
        path : Path
            image/image_id.jpg e.g image/000420.jpg
        zfill : int, optional
            the specified length to stop adding zeros (0) at the beginning of the string , by default 6
        """
        self.image_id = image_id
        self.image_path = path.as_posix()


@dataclass
class Color:
    name: str
    hex_value: str

    def __post_init__(self):
        self.rgb_tuple = tuple(hex_to_rgb(self.hex_value))


def generate_datapoint(height, width) -> Datapoint:
    """Generate a random circle on a random background

    The circle is guaranteed to be inside the image fully

    Parameters
    ----------
    height : int
        height of the image
    width : int
        width of the image

    Returns
    -------
    Datapoint
        An object with the following attributes:
            image
            circle_color_name
            background_color_name
    """

    # Create two Color, the former is for the full circle, the latter is for the background
    color_list = random.sample(list(CSS3_NAMES_TO_HEX.items()), 2)
    color_list = [Color(i[0], i[1]) for i in color_list]

    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Paint the background
    image[:, :] = color_list[1].rgb_tuple

    # Paint the full circle
    radius = random.randint(1, min(height, width) // 2)
    center = (
        random.randint(radius, height - radius),
        random.randint(radius, width - radius),
    )
    rr, cc = disk(center, radius, shape=(height, width))
    image[rr, cc] = color_list[0].rgb_tuple

    return Datapoint(
        image=image,
        circle_color_name=color_list[0].name,
        background_color_name=color_list[1].name,
    )


if __name__ == '__main__':
    seed = 42
    random.seed(seed)
    np.random.seed(seed)

    demo_path = Path('demo.jpg')
    dp = generate_datapoint(256, 256)
    dp.make_caption()
    dp.make_question_answer_list()
    dp.make_id_path('demo', demo_path)

    imsave(dp.image_path, dp.image, check_contrast=False)
    print(json.dumps(dp.to_dict(exclude=('image')), indent=4))
