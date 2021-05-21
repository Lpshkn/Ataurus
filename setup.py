import ataurus
from os.path import join, dirname
from setuptools import setup, find_packages
from ataurus.console_handle.console_handler import ConsoleHandler

setup(
    name=ConsoleHandler.NAME,
    version=ataurus.__version__,
    packages=find_packages(),
    url='https://github.com/Lpshkn/Ataurus/',
    license='',
    author='lpshkn',
    test_suite="tests",
    author_email='lepkirill@yandex.ru',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    description=ConsoleHandler.DESCRIPTION,
    entry_points={
        'console_scripts': ['ataurus = ataurus.main:main']
    }
)
