#!/usr/bin/env python

"""
Deployment file to facilitate releases of monty.
"""
from __future__ import annotations

import datetime
import glob
import json
import os
import re

import requests
from invoke import task

from monty import __version__ as ver
from monty.os import cd

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyue@mit.edu"
__date__ = "Apr 29, 2012"

NEW_VER = datetime.datetime.today().strftime("%Y.%-m.%-d")


@task
def make_doc(ctx):
    with cd("docs"):
        ctx.run("rm monty.*.rst", warn=True)
        ctx.run("sphinx-apidoc --separate -P -M -d 6 -o . -f ../monty")
        # ctx.run("rm monty*.html", warn=True)
        # ctx.run("sphinx-build -b html . ../docs")  # HTML building.
        ctx.run("sphinx-build -M markdown . .")
        ctx.run("rm *.rst", warn=True)
        ctx.run("cp markdown/monty*.md .")
        for fn in glob.glob("monty*.md"):
            with open(fn) as f:
                lines = [line.rstrip() for line in f if "Submodules" not in line]
            if fn == "monty.md":
                preamble = [
                    "---",
                    "layout: default",
                    "title: API Documentation",
                    "nav_order: 5",
                    "---",
                    "",
                ]
            else:
                preamble = [
                    "---",
                    "layout: default",
                    "title: " + fn,
                    "nav_exclude: true",
                    "---",
                    "",
                ]
            with open(fn, "w") as f:
                f.write("\n".join(preamble + lines))

        ctx.run("rm -r markdown", warn=True)
        ctx.run("cp ../*.md .")
        ctx.run("mv README.md index.md")
        ctx.run("rm -rf *.orig doctrees", warn=True)

        with open("index.md") as f:
            contents = f.read()
        with open("index.md", "w") as f:
            contents = re.sub(
                r"\n## Official Documentation[^#]*",
                "{: .no_toc }\n\n## Table of contents\n{: .no_toc .text-delta }\n* TOC\n{:toc}\n\n",
                contents,
            )
            contents = (
                "---\nlayout: default\ntitle: Home\nnav_order: 1\n---\n\n" + contents
            )

            f.write(contents)


@task
def update_doc(ctx):
    ctx.run("git pull", warn=True)
    make_doc(ctx)
    ctx.run("git add .", warn=True)
    ctx.run('git commit -a -m "Update dev docs"', warn=True)
    ctx.run("git push", warn=True)


@task
def test(ctx):
    ctx.run("pytest")


@task
def setver(ctx):
    ctx.run(f'sed s/version=.*,/version=\\"{ver}\\",/ setup.py > newsetup')
    ctx.run("mv newsetup setup.py")


@task
def release_github(ctx):
    with open("docs/changelog.md") as f:
        contents = f.read()
    toks = re.split("##", contents)
    desc = toks[1].strip()
    payload = {
        "tag_name": "v" + NEW_VER,
        "target_commitish": "master",
        "name": "v" + NEW_VER,
        "body": desc,
        "draft": False,
        "prerelease": False,
    }

    response = requests.post(
        "https://api.github.com/repos/materialsvirtuallab/monty/releases",
        data=json.dumps(payload),
        headers={"Authorization": "token " + os.environ["GITHUB_RELEASES_TOKEN"]},
    )
    print(response.text)


@task
def commit(ctx):
    ctx.run('git commit -a -m "v%s release"' % NEW_VER, warn=True)
    ctx.run("git push", warn=True)


@task
def set_ver(ctx):
    with open("monty/__init__.py") as f:
        contents = f.read()
        contents = re.sub(
            r"__version__ = .*\n", '__version__ = "%s"\n' % NEW_VER, contents
        )

    with open("monty/__init__.py", "w") as f:
        f.write(contents)

    with open("pyproject.toml") as f:
        contents = f.read()
        contents = re.sub(
            r"version = ([\.\d\"]+)", 'version = "%s"' % NEW_VER, contents
        )

    with open("pyproject.toml", "w") as f:
        f.write(contents)


@task
def release(ctx, notest=False):
    set_ver(ctx)
    if not notest:
        test(ctx)
    update_doc(ctx)
    commit(ctx)
    release_github(ctx)
    ctx.run("python -m build", warn=True)
    ctx.run("python -m build --wheel", warn=True)
    ctx.run("twine upload --skip-existing dist/*.whl", warn=True)
    ctx.run("twine upload --skip-existing dist/*.tar.gz", warn=True)
