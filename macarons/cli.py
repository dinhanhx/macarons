import click
from pathlib import Path
from macarons.dataset import build


@click.command()
@click.option(
    '--output_dir', default='', help='where the dataset directory should be contained'
)
@click.option('--image_height', default=224, help='the image height')
@click.option('--image_width', default=224, help='the image width')
@click.option('--amount', default=1000, help='number of samples')
@click.option('--task', default='all', help='dataset type')
@click.option('--seed', default=42, help='random seed')
def main(output_dir, image_height, image_width, amount, task, seed):
    """Build dataset

    Available tasks: all, image caption, visual question answer
    """
    build(Path(output_dir), (image_height, image_width), amount, task, seed)


if __name__ == '__main__':
    main()
