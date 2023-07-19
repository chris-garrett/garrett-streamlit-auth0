import re
from typing import NamedTuple
import subprocess


def exec(cmd, timeout=1):
    return subprocess.run(cmd.split(), capture_output=True, text=True, timeout=timeout)


def git_version():
    descr = exec("git describe").stdout.strip()
    ret = re.search(r"(\d+).(\d+).(\d+)-(\d+)-g([0-9a-zA-Z]+)", descr)
    return NamedTuple(
        "GitVersion",
        [
            ("major", str),
            ("minor", str),
            ("patch", str),
            ("commit", str),
            ("hash", str),
        ],
    )(
        major=ret.group(1),
        minor=ret.group(2),
        patch=ret.group(3),
        commit=ret.group(4),
        hash=ret.group(5),
    )


def git_version_semver():
    gv = git_version()
    return f"{gv.major}.{gv.minor}.{gv.patch}+{gv.commit}"
