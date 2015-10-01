from setuptools import setup, find_packages
from io import open

with open("README.md", "rt") as f:
    long_desc = f.read()

setup(
    name="monty",
    packages=find_packages(),
    version="0.6.6",
    install_requires=["six"],
    extras_require={"yaml": ["pyyaml>=3.1"],},
    package_data={},
    author="Shyue Ping Ong",
    author_email="ongsp@ucsd.edu",
    maintainer="Shyue Ping Ong",
    url="https://github.com/materialsvirtuallab/monty",
    license="MIT",
    description="Monty is the missing complement to Python.",
    long_description=long_desc,
    keywords=["monty"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
