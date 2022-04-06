import os

from depixelizer.io import read_png, get_writer
from .pixel_data import PixelData

class Depixelize():
    def __init__(self, filename, output_dir=None):
        self.filename = filename
        if output_dir:
            self.output_dir = output_dir
        else:
            self.output_dir = os.getcwd()
    
    def run(self):
        self.pixel_data = PixelData(read_png(self.filename))
        file_name = os.path.basename(self.filename).split(".")[0]
        self.pixel_data.depixelize()
        output_filepath = os.path.join(self.output_dir, file_name)
        writer = get_writer(self.pixel_data, output_filepath)
        writer.output_image()
        