#!/usr/bin/env python

import setuptools

import problemdetails

setuptools.setup(
    name='tornado-problem-details',
    version=problemdetails.version,
    description='RFC-7807 Error documents for Tornado',
    long_description=open('README.rst').read(),
    author='Dave Shawley',
    author_email='daveshawley@gmail.com',
    url='https://github.com/dave-shawley/tornado-problem-details',
    packages=['problemdetails'],
    install_requires=[
        'tornado>=4.4',
    ],
    extras_require={
        'dev': [
            'coverage==4.5.3',
            'flake8==3.7.7',
            'flake8-fixme==1.1.0',
            'flake8-print==3.1.0',
            'nose==1.3.7',
            'readme-renderer==24.0',
            'sphinx==2.0.0',
            'tox==3.8.4',
            'twine==1.13.0',
            'wheel==0.33.1',
            'yapf==0.26.0',
        ],
        'docs': [
            'sphinx==2.0.0',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries',
    ],
)
