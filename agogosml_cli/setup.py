#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open("requirements.txt") as requirements_file:
    requirements = [line.strip() for line in requirements_file]

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
    description="Agogosml cli project to scaffold and generate an agogosml project.",
    entry_points={
        'console_scripts': [
            'agogosml=cli.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='agogosml_cli',
    name='agogosml_cli',
    packages=find_packages(include=['agogosml_cli', 'cli']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Microsoft/agogosml/agogosml_cli',
    version='0.1.2',
    zip_safe=False,
)
