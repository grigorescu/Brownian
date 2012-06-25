from setuptools import setup
setup(
    name = "Brownian",
    version = "0.1",
    packages = ["Brownian", "Brownian.view", "Brownian.view.utils"],
    install_requires = ["Django", "requests"],
    package_data = {'Brownian.view':
                        ['static/css/*.css',
                         'static/img/*.png',
                         'static/js/*.js',
                         'templates/*.html',
                         'templates/include/*.html',
                        ]},
    include_package_data = True,
    zip_safe = False,
)