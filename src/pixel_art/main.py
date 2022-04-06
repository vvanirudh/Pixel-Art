from input import read_png
import output
import os.path
import argparse

from algorithm import PixelData


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    if len(args.path) > 0:
        filename = args.path
    else:
        filename = input(
            "Please Enter the name of the png file (with extension)")

    process_file(filename)


def process_file(filename):
    data = PixelData(read_png(filename))
    filename_without_extension = os.path.splitext(
        os.path.split(filename)[-1])[0]
    # filename_without_extension = filename.split(".")[0]

    data.depixelize()

    writer = output.get_writer(data, filename_without_extension)
    writer.output_image()


if __name__ == '__main__':
    main()
