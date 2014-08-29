#!/usr/bin/env python

"""
Deployment file to facilitate releases of monty.
"""

from __future__ import division

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyue@mit.edu"
__date__ = "Apr 29, 2012"

import glob
import requests
import json
import os

from fabric.api import local, lcd
from monty import __version__ as ver


def makedoc():
    with lcd("docs"):
        local("sphinx-apidoc -o . -f ../monty")
        for f in glob.glob("docs/*.rst"):
            if f.startswith('docs/monty') and f.endswith('rst'):
                newoutput = []
                suboutput = []
                subpackage = False
                with open(f, 'r') as fid:
                    for line in fid:
                        clean = line.strip()
                        if clean == "Subpackages":
                            subpackage = True
                        if not subpackage and not clean.endswith("tests"):
                            newoutput.append(line)
                        else:
                            if not clean.endswith("tests"):
                                suboutput.append(line)
                            if clean.startswith("monty") and not clean.endswith("tests"):
                                newoutput.extend(suboutput)
                                subpackage = False
                                suboutput = []

                with open(f, 'w') as fid:
                    fid.write("".join(newoutput))
        local("make html")

        #This makes sure monty.org works to redirect to the Gihub page
        local("echo \"monty.org\" > _build/html/CNAME")
        #Avoid ths use of jekyll so that _dir works as intended.
        local("touch _build/html/.nojekyll")


def publish():
    local("python setup.py release")


def test():
    local("nosetests")


def setver():
    local("sed s/version=.*,/version=\\\"{}\\\",/ setup.py > newsetup"
          .format(ver))
    local("mv newsetup setup.py")


def release_github():
    desc = []
    read = False
    with open("docs/index.rst") as f:
        for l in f:
            if l.strip() == "v" + ver:
                read = True
            elif l.strip() == "":
                read = False
            elif read:
                desc.append(l.rstrip())
    desc.pop(0)
    payload = {
        "tag_name": "v" + ver,
        "target_commitish": "master",
        "name": "v" + ver,
        "body": "\n".join(desc),
        "draft": False,
        "prerelease": False
    }

    response = requests.post(
        "https://api.github.com/repos/materialsvirtuallab/monty/releases",
        data=json.dumps(payload),
        headers={"Authorization": "token " + os.environ["PYMATGEN_GH_TOKEN"]})
    print response.text


def release():
    setver()
    test()
    makedoc()
    publish()
    release_github()
