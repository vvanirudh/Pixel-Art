DEPIXELIZING PIXEL ART
======================

An implementation of the paper *Depixelizing Pixel Art* by Kopf and Lischinski. The implementation is purely in python and instructions are given below.

![example_image](outputs/win31_setup_input.svg)

Instructions to run

<pre><code>
    from pixel_art import Depixelize
    Depixelize(input_image_path, output_dir).run()
</code></pre>

Requirements
============
- Python
- `pypng` : https://pypi.python.org/pypi/pypng
- `networkx`: https://pypi.python.org/pypi/networkx/
- `svgwrite` : https://pypi.python.org/pypi/svgwrite/

Citations
=========

- https://johanneskopf.de/publications/pixelart/paper/pixel.pdf
- https://github.com/gityou/depixelize
- http://dev.crazyrobot.net/2011/07/12/pixelart-to-vector/
- https://code.launchpad.net/libdepixelize
- http://networkx.lanl.gov/index.html
- https://github.com/jerith/depixel
- https://svgwrite.readthedocs.org/en/latest/
- http://vinipsmaker.wordpress.com/2013/07/21/splines-extraction-on-kopf-lischinski-algorithm-part-1/
- http://vinipsmaker.wordpress.com/2013/08/13/splines-extraction-on-kopf-lischinski-algorithm-part-2/

Authors
=======
*Anirudh Vemula, Vamsidhar Yeddu*

Computer Science & Engineering, IIT Bombay
