#!/usr/bin/env python

"""
Deployment file to facilitate releases of monty.
"""


import glob
import requests
import json
import os

from invoke import task
from monty.os import cd
from monty import __version__ as ver


__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyue@mit.edu"
__date__ = "Apr 29, 2012"


@task
def make_doc(ctx):
    with cd("docs_rst"):
        ctx.run("sphinx-apidoc --separate -d 6 -o . -f ../monty")
        for f in glob.glob("*.rst"):
            if f.startswith('monty') and f.endswith('rst'):
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
                            if clean.startswith(
                                    "monty") and not clean.endswith("tests"):
                                newoutput.extend(suboutput)
                                subpackage = False
                                suboutput = []

                with open(f, 'w') as fid:
                    fid.write("".join(newoutput))
        ctx.run("make html")

        # ctx.run("cp _static/* ../docs/html/_static")

    with cd("docs"):
        ctx.run("cp -r html/* .")
        ctx.run("rm -r html")
        ctx.run("rm -r doctrees")
        ctx.run("rm -r _sources")

        # This makes sure pymatgen.org works to redirect to the Gihub page
        # ctx.run("echo \"pymatgen.org\" > CNAME")
        # Avoid the use of jekyll so that _dir works as intended.
        ctx.run("touch .nojekyll")


@task
def update_doc(ctx):
    ctx.run("git pull", warn=True)
    make_doc(ctx)
    ctx.run("git add .", warn=True)
    ctx.run("git commit -a -m \"Update dev docs\"", warn=True)
    ctx.run("git push", warn=True)


@task
def publish(ctx):
    ctx.run("rm dist/*.*", warn=True)
    ctx.run("python setup.py sdist bdist_wheel")
    ctx.run("twine upload dist/*")


@task
def test(ctx):
    ctx.run("pytest")


@task
def setver(ctx):
    ctx.run("sed s/version=.*,/version=\\\"{}\\\",/ setup.py > newsetup"
          .format(ver))
    ctx.run("mv newsetup setup.py")


@task
def release_github(ctx):
    desc = []
    read = False
    with open("docs_rst/index.rst") as f:
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
    ctx.run("git commit -a -m \"v%s release\"" % ver, warn=True)
    ctx.run("git push", warn=True)


@task
def release(ctx):
    # setver(ctx)
    test(ctx)
    update_doc(ctx)
    publish(ctx)
    commit(ctx)
    release_github(ctx)
