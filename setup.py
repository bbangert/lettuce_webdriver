__version__ = '0.3.1'

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
        'Topic :: Software Development :: Testing',
        ],
      keywords='web lettuce bdd',
      author="Nick Pilon, Ben Bangert",
      author_email="npilon@gmail.com, ben@groovie.org",
      url="https://github.com/bbangert/lettuce_webdriver/",
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require = ['lettuce', 'selenium'],
      install_requires=['lettuce','selenium>=2.8.1'],
      test_suite="lettuce_webdriver",
      )
