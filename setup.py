import authorship_attribution
from os.path import join, dirname
from setuptools import setup, find_packages


setup(
    name='AuthorshipAttribution',
    version=authorship_attribution.__version__,
    packages=find_packages(),
    url='https://github.com/Nikshepel/AuthorshipAttribution',
    license='',
    author='lpshkn',
    test_suite="tests",
    author_email='lepkirill@yandex.ru',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    description='This program collects data from the sites(optional), processes this data, '
                'gets the parameter vector from the data and trains the model of machine learning to specify '
                'the author of an unknown text.'
)