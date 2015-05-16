"""
Based entirely on Django's own ``setup.py``.
"""
import os
import sys

from setuptools import setup, find_packages

PACKAGE_NAME = 'navutils'

version = __import__(PACKAGE_NAME).__version__

setup(
    name='django-navutils',
    version=version,
    description="Navigation utils for Django",
    long_description="""django-navutils bundles several tools for building consistent navigation
    in a Django project""",
    author='Eliot Berriot',
    author_email='contact@eliotberriot.com',
    maintainer='Eliot Berriot',
    maintainer_email='contact@eliotberriot.com',
    url='http://github.com/EliotBerriot/django-navutils',
    license='MIT License',
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['persisting_theory'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
