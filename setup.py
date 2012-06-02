#!/usr/bin/env python
"""
redis-contrib
======

Missing contrib packages for redis-py.
"""

from setuptools import setup, find_packages

setup(
    name='redis-contrib',
    version='0.0.0',
    author='Matt Robenolt',
    author_email='matt@ydekproductions.com',
    url='https://github.com/mattrobenolt/redis-py-contrib',
    description='Missing contrib packages for redis-py',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    license='BSD',
    install_requires=[
        'redis',
    ],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
