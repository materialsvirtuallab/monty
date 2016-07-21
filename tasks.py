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

from invoke import task
from monty.os import cd
from monty import __version__ as ver


@task
def make_doc(ctx):
    with cd("docs"):
        ctx.run("sphinx-apidoc -o . -f ../monty")
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
        ctx.run("make html")

        #This makes sure monty.org works to redirect to the Gihub page
        ctx.run("echo \"monty.org\" > _build/html/CNAME")
        #Avoid ths use of jekyll so that _dir works as intended.
        ctx.run("touch _build/html/.nojekyll")


@task
def publish(ctx):
    ctx.run("python setup.py release")


@task
def test(ctx):
    ctx.run("nosetests")


@task
def setver(ctx):
    ctx.run("sed s/version=.*,/version=\\\"{}\\\",/ setup.py > newsetup"
          .format(ver))
    ctx.run("mv newsetup setup.py")


@task
def release_github(ctx):
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
        headers={"Authorization": "token " + os.environ["GITHUB_RELEASES_TOKEN"]})
    print(response.text)


@task
def commit(ctx):
    ctx.run("git commit -a -m \"v%s release\"" % ver)
    ctx.run("git push")


@task
def release(ctx):
    setver(ctx)
    test(ctx)
    make_doc(ctx)
    publish(ctx)
    commit(ctx)
    release_github(ctx)
