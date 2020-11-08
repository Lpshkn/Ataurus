import ataurus
from os.path import join, dirname
from setuptools import setup, find_packages
from ataurus.configurator import Configurator

setup(
    name=Configurator.NAME,
    version=ataurus.__version__,
    packages=find_packages(),
    url='https://github.com/Nikshepel/AuthorshipAttribution',
    license='',
    author='lpshkn',
    test_suite="tests",
    author_email='lepkirill@yandex.ru',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    description=Configurator.DESCRIPTION,
    entry_points={
        'console_scripts': ['Ataurus = ataurus.main:main']
    }
)
