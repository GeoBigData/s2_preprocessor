#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Michael Gleason",
    author_email='michael.gleason@digitalglobe.com',
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
        'Programming Language :: Python :: 3.7',
    ],
    description="Python module wrapping SentinelHub Python API and SNAP tools for GBDX task deployment",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='s2_preprocessor',
    name='s2_preprocessor',
    packages=find_packages(include=['s2_preprocessor']),
    setup_requires=setup_requirements,
    entry_points='''[console_scripts]
                    compile_archive=s2_preprocessor.compile_archive:main
                    L2A_process=s2_preprocessor.L2A_process:main''',
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/GeoBigData/s2_preprocessor',
    version='0.0.1',
    zip_safe=False,
)
