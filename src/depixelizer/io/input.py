import png  # pypng


def read_png(filename):
    width, height, pixels, metadata = png.Reader(
        filename=filename
    ).asRGB8()  # Get the pixel data as RGB with 8 bits each
    pixel_data = []

    for pixel_row in pixels:  # For each row in the image
        pixel = []
        while pixel_row:
            pixel.append(
                (pixel_row.pop(0), pixel_row.pop(0), pixel_row.pop(0))
            )  # Get the RGB value of the pixel
        pixel_data.append(pixel)
    return pixel_data
