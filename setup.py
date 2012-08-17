from setuptools import setup
setup(
    name = "Brownian",
    version = "0.4-r82",
    packages = ["Brownian", "Brownian.view", "Brownian.view.templatetags", "Brownian.view.utils"],
    install_requires = ["Django==1.4", "django-dajax==0.8.4", "django-dajaxice==0.2", "requests", "nose", "pytz"],
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