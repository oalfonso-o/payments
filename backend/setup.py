from setuptools import setup
from setuptools import find_packages

__version__ = '0.0.1'

setup(
    name='oalfonso-payments',
    version=__version__,
    long_description='Allows handling and transfering money with friends.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django<=3.0',
        'psycopg2-binary<=2.9',
        'python-dotenv==0.10.2',
        'djangorestframework<=3.10',
        'django-cors-headers<3.1',
        'django-money==0.15',
        'bcrypt<3.2',
        'django-model-utils<3.2',
    ],
)
