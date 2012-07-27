from setuptools import setup
setup(
    name = "Brownian",
    version = "0.4-r69",
    packages = ["Brownian", "Brownian.view", "Brownian.view.templatetags", "Brownian.view.utils"],
    install_requires = ["Django", "django-dajax", "django-dajaxice", "requests", "nose", "pytz"],
    package_data = {'Brownian.view':
                        ['static/css/*.css',
                         'static/img/*.png',
                         'static/img/*.gif',
                         'static/js/*.js',
                         'templates/*.html',
                         'templates/include/*.html',
                        ]},
    include_package_data = True,
    zip_safe = False,
    test_suite = "Brownian.view.tests",
)