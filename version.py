#
# To simplify versioning I'm going to do the following:
# * Every merge to main:  bump the minor version
# * There will be no "patches".
# * Major version bumps will be a manual commit + tag to main
# main   == 1.0, 1.1...
# cg/foo == 1.0.dev<timestamp>
#
import re
import time
from typing import NamedTuple
import subprocess


def exec(cmd, timeout=1):
    return subprocess.run(cmd.split(), capture_output=True, text=True, timeout=timeout)


def git_version():
    branch = (
        exec("git rev-parse --abbrev-ref HEAD")
        .stdout.strip()
        .replace("/", ".")
        .replace("-", ".")
    )

    descr = exec("git describe").stdout.strip()
    ret = re.search(r"(\d+).(\d+)-(\d+)-g([0-9a-zA-Z]+)", descr)

    return NamedTuple(
        "GitVersion",
        [
            ("major", int),
            ("minor", int),
            ("commit", int),
            ("hash", str),
            ("branch", str),
        ],
    )(
        major=int(ret.group(1)),
        minor=int(ret.group(2)),
        commit=int(ret.group(3)),
        hash=ret.group(4),
        branch=branch,
    )


def get_version():
    gv = git_version()
    return (
        f"{gv.major}.{gv.minor}"
        if gv.branch == "main"
        else f"{gv.major}.{gv.minor}.dev{int(time.time())}"
    )


def get_next_version():
    gv = git_version()
    return (
        f"{gv.major}.{gv.minor + 1}"
        if gv.branch != "main"
        else f"{gv.major}.{gv.minor}.dev{int(time.time())}"
    )
