__version__ = '0.1'

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

setup(name='lettuce_webdriver',
      version=__version__,
      description='Selenium webdriver extension for lettuce',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        ],
      keywords='web lettuce bdd',
      author="Ben Bangert",
      author_email="ben@groovie.org",
      url="",
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require = ['lettuce', 'selenium'],
      install_requires=['lettuce','selenium>=2.0b2'],
      test_suite="lettuce_webdriver",
      )
