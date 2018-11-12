#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

# TODO: Uncomment the history part when publish
# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Rami Sayar",
    author_email='rami.sayar@microsoft.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Agogosml Library",
    install_requires=requirements,
    license="MIT license",
    #long_description=readme + '\n\n' + history, # TODO: Uncomment the history part when publish
    include_package_data=True,
    keywords='agogosml',
    name='agogosml',
    packages=find_packages(include=['agogosml**']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Microsoft/agogosml',
    version='0.1.0',
    zip_safe=False,
)
