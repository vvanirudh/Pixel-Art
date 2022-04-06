from importlib.metadata import entry_points
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="depixelizer",
    version="0.0.1",
    author="Anirudh Vemula, Vamsidhar Yeddu",
    author_email="vvanirudh@gmail.com, vamsidhar666@gmail.com",
    description="An implementation of the paper Depixelizing Pixel Art by Kopf and Lischinski.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vvanirudh/Pixel-Art",
    project_urls={
        "Bug Tracker": "https://github.com/vvanirudh/Pixel-Art/issues",
    },
    entry_points={
        "console_scripts": ["depixelize=depixelizer.cmd:depixelize_fn"],
    },
    classifiers=["Programming Language :: Python :: 3"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
