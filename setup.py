from setuptools import setup, find_packages
setup(
    name = "Brownian",
    version = "0.1",
    packages = find_packages(),
    install_requires = ["Django", "requests"],
    package_data = {'view':
                        ['static/css/*.css',
                         'static/img/*.png',
                         'static/js/*.js',
                         'templates/*.html',
                         'templates/include/*.html',
                        ]},
    include_package_data = True,
    zip_safe = False,
)