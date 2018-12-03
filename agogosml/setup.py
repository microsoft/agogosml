#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "confluent-kafka==0.11.6",
    "azure-eventhub==1.2.0",
    "requests==2.20.1",
    "python-dotenv==0.9.1",
    "flask==1.0.2",
    "pyyaml==3.13",
    "jsonschema==2.6.0"
]

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
        'Programming Language :: Python :: 3.7'
    ],
    description="Agogosml Library",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
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
