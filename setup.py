import os
import sys

from setuptools import setup, Command

class PyTest(Command):
    """
    A command to convince setuptools to run pytests.
    """
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import pytest
        errno = pytest.main("test.py")
        sys.exit(errno)

requirements = open('requirements.txt').read().split()

setup(
    name = 'ndnp_iiif',
    version = '0.0.1',
    url = 'http://github.com/umd-mith/ndnp_iiif',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['ndnp_iiif'],
    scripts = ['bin/ndnp_iiif'],
    description = 'convert ndnp data to iiif',
    test_suite = 'test',
    install_requires = requirements,
    cmdclass = {'test': PyTest},
    tests_require = ['pytest'],
)
