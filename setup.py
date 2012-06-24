from setuptools import setup, find_packages
setup(
    name = "Brownian",
    version = "0.1",
    packages = find_packages(),
    install_requires = ["Django", "requests"],
    package_data = {'': ["*.js", "*.css", "*.png", "*.html"]},
    include_package_data = True,

)