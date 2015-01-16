#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="k-state-tests",
    packages = find_packages(),
    version = "0.0.1b0",
    install_requires = [
        "django",
        "celery",
        "six"
    ],
    tests_require = [
        "pytest>=2.6.1",
        "pytest-cov>=1.7.0",
        "pytest-django>=2.6.2",
    ],
)
