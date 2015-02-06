import os
from setuptools import setup
from setuptools import find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(name='comicstrip',
      version='0.1',
      author='mozillamonks',
      author_email='hi@robinmonks.com',
      description='Extract individual frames of a comic book',
      long_description=read('README'),
      packages=find_packages()
)
