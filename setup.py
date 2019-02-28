from setuptools import setup

setup(name='fruit',
      version='0.1',
      url='http://github.com/eivindbergem/fruit',
      author='Eivind Alexander Bergem',
      author_email='eivind.bergem@gmail.com',
      license='GPL',
      packages=['fruit'],
      test_suite='nose.collector',
      tests_require=['nose'])
