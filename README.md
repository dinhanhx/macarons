# Macarons

A tool to generate image-text data. The following tasks are supported:
- image caption
- visual question answer
- all of them

# Setup

You need to `git clone` the repo first because I won't upload this to PyPI

With good old pip
```
pip install -e .
```

With fancy poetry
```
poetry install
```

# Demo

![The darkmagenta circle on the bisque background](demo.jpg)

Here is a single data point for all of them task. This json can be different depend on the task.
- for task image caption, there is no `question_answer_list`
- for task visual question answer, there is no `caption`

```json
{
    "circle_color_name": "darkmagenta",
    "background_color_name": "bisque",
    "caption": "The darkmagenta circle on the bisque background",
    "question_answer_list": [
        [
            "What is the color of the circle",
            "darkmagenta"
        ],
        [
            "What is the color of the background",
            "bisque"
        ],
        [
            "What are the color of the circle and the background",
            "darkmagenta and bisque"
        ]
    ],
    "image_id": "demo",
    "image_path": "demo.jpg"
}
```

# Usage

**NOTE**: `macarons.dataset.build()` function build the dataset folder **inside** user-defined folder. For example,
you give the function this path `demo_data`. Then it will create `demo_data/data` which contain `map.jsonl` file and `image` folder. All the paths recorded in `map.jsonl` are relative to `image/` folder solely.

## Via API
```python
import random
from pathlib import Path
import json

import numpy as np
from skimage.io import imsave

from macarons.dataset import build, TASKS
from macarons.image_text import generate_datapoint

seed = 42
random.seed(seed)
np.random.seed(seed)

# Generate a single data point
demo_path = Path('demo.jpg')
dp = generate_datapoint(256, 256)
dp.make_caption()
dp.make_question_answer_list()
dp.make_id_path('demo', demo_path)

imsave(dp.image_path, dp.image, check_contrast=False)
print(json.dumps(dp.to_dict(exclude=('image')), indent=4))

# Generate all tasks
for task in TASKS:
    build(Path(f'demo_data/{task}'), amount=10, task=task)

```

## Via CLI

WIP