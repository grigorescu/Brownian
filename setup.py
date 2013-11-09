from setuptools import setup

from Brownian import __version__

setup(
    name="Brownian",
    version=__version__,
    packages=["Brownian"],
    install_requires=["flask==0.9", "requests==1.1.0"],
)
