from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(
    name="monty",
    packages=find_packages(),
    version="0.0.1",
    install_requires=[],
    extras_require={},
    package_data={},
    author="materials virtual lab",
    author_email="",
    maintainer="materials virtual lab",
    url="https://github.com/materialsvirtuallab/monty",
    license="MIT",
    description="Monty is the missing complement to Python.",
    long_description="Monty implements supplementary useful functions for "
                     "Python that are not part of the standard library. "
                     "Examples include useful utilities like transparent "
                     "support for zipped files etc.",
    keywords=["monty"],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
