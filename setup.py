#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="DTAutomator",
    version="0.0.1",
    author="HsOjo",
    author_email="hsojo@qq.com",
    keywords='hsojo python3 android automator dtautomator',
    description='''Droid Test Automator SDK.''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HsOjo/DTAutomator/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
