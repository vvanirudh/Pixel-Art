from depixelizer import Depixelize
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("image_path", help="Input Pixel Art Image")
parser.add_argument(
    "--output_dir",
    default=None,
    required=False,
    help="Output Dir, defaults to os.cwd()",
)


def depixelize_fn():
    args = parser.parse_args()
    if len(args.image_path) > 0:
        filename = args.image_path
    else:
        filename = input("Please enter the input image path")
    Depixelize(filename, args.output_dir).run()
