import os
from setuptools import setup, find_packages
import io

current_dir = os.path.dirname(os.path.abspath(__file__))

with io.open(os.path.join(current_dir, "README.rst"), "rt") as f:
    long_desc = f.read()

setup(
    name="monty",
    packages=find_packages(),
    version="2022.1.19",
    extras_require={
        "yaml": ["ruamel.yaml"],
    },
    package_data={},
    author="Shyue Ping Ong",
    author_email="ongsp@ucsd.edu",
    maintainer="Shyue Ping Ong",
    url="https://github.com/materialsvirtuallab/monty",
    license="MIT",
    description="Monty is the missing complement to Python.",
    long_description=long_desc,
    keywords=["monty"],
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
