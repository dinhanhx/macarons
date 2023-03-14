# Macarons

A tool to generate image-text data. The following tasks are supported:
- image caption
- visual question answer
- all of them

# Setup

You need to `git clone` the repo first because I won't upload this package to PyPI

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
you give the function this path `demo_data`. Then it will create `demo_data/macarons-{task}` which contain `map.jsonl` file and `image` folder. All the paths recorded in `map.jsonl` are relative to `image/` folder solely.

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
    build(Path('demo_data'), amount=10, task=task)

```

## Via CLI

### Ask for help
Command:
```bash
python -m macarons.cli --help
```
Output:
```text
Usage: python -m macarons.cli [OPTIONS]

  Build dataset

  Available tasks: all, image caption, visual question answer

Options:
  --output_dir TEXT       where the dataset directory should be contained
                          [default: .]
  --image_height INTEGER  the image height  [default: 224]
  --image_width INTEGER   the image width  [default: 224]
  --amount INTEGER        number of samples  [default: 1000]
  --task TEXT             dataset type  [default: all]
  --seed INTEGER          random seed  [default: 42]
  --help                  Show this message and exit.
```

### Example
```bash
python -m macarons.cli --output_dir=data --amount=10
```