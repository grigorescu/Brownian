from setuptools import setup
setup(
    name = "Brownian",
    version = "0.4-r99",
    packages = ["Brownian", "Brownian.view", "Brownian.view.templatetags", "Brownian.view.utils"],
    install_requires = ["Django==1.4.1", "django-dajax==0.9.1", "django-dajaxice==0.5", "requests==0.13.6", "nose", "pytz"],
    package_data = {'Brownian.view':
                        ['static/css/*.css',
                         'static/img/*.png',
                         'static/img/*.gif',
                         'static/js/*.js',
                         'static/dajaxice/*.js',
                         'templates/*.html',
                         'templates/include/*.html',
                        ]},
    include_package_data = True,
    zip_safe = False,
    test_suite = "Brownian.view.tests",
)
