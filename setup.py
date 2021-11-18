import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trackee",
    version="0.0.1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[f"plotbee @ file://localhost/{os.getcwd()}/plotbee#egg=plotbee", "ipywidgets"],
    python_requires='>=3.6',
)
