"""
Based entirely on Django's own ``setup.py``.
"""
import os
import sys
import codecs
import re
from setuptools import setup, find_packages

PACKAGE_NAME = 'navutils'

def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-navutils',
    version=find_version(PACKAGE_NAME, '__version__.py'),
    description="A lightweight package for handling menus and breadcrumbs in your django project",
    long_description=read('README.rst'),
    author='Eliot Berriot',
    author_email='contact@eliotberriot.com',
    maintainer='Eliot Berriot',
    maintainer_email='contact@eliotberriot.com',
    url='http://github.com/EliotBerriot/django-navutils',
    license='BSD License',
    platforms=['any'],
    packages=find_packages(),
    package_data = {
        'navutils': [
            'templates/navutils/*.html',
        ],
    },
    include_package_data=True,
    install_requires=['persisting_theory'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Topic :: Utilities',
    ],
)
