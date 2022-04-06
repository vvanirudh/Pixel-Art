import os

from pixel_art.io import read_png, get_writer
from .pixel_data import PixelData

class Depixelize():
    def __init__(self, filename, output_dir):
        self.filename = filename
        self.output_dir = output_dir
    
    def run(self):
        self.pixel_data = PixelData(read_png(self.filename))
        file_name = os.path.basename(self.filename).split(".")[0]
        self.pixel_data.depixelize()
        output_filepath = os.path.join(self.output_dir, f"{file_name}.svg")
        writer = get_writer(self.pixel_data, output_filepath)
        writer.output_image()
        