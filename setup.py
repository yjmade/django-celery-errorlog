#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys

if 'sdist' in sys.argv:
    from pypandoc import convert
    long_description = convert('README.md', 'rst')
else:
    long_description = ""
VERSION = "0.1.1"

setup(
    name='django-celery-errorlog',
    version=VERSION,
    description='Reuseable app for django to collect the unexpted exception and generate comprehansive report just like what you get in debug mode and store in database from celery task',
    url="https://github.com/yjmade/django-celery-errorlog",
    long_description=long_description,
    author='Jay Young(yjmade)',
    author_email='dev@yjmade.net',
    packages=find_packages(),
    install_requires=["django-celery", "django-errorlog"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='MIT',
    keywords='django celery error log report',

)
