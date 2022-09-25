# -*- coding: utf-8 -*-

from ast import parse
from distutils.sysconfig import get_python_lib
from functools import partial
from operator import attrgetter, itemgetter
from os import listdir, path
from sys import version_info

from setuptools import find_packages, setup

if version_info[0] == 2:
    from itertools import ifilter as filter
    from itertools import imap as map

if __name__ == "__main__":
    package_name = "offregister_web_servers"

    f_for = partial(path.join, path.dirname(__file__), package_name)
    d_for = partial(path.join, get_python_lib(), package_name)

    nginx_data = partial(path.join, f_for("nginx", "data"))
    nginx_install_dir = partial(path.join, d_for("nginx", "data"))

    with open(path.join(package_name, "__init__.py")) as f:
        __author__, __version__ = map(
            lambda const: const.value if hasattr(const, "value") else const.s,
            map(
                attrgetter("value"),
                map(
                    itemgetter(0),
                    map(
                        attrgetter("body"),
                        map(
                            parse,
                            filter(
                                lambda line: line.startswith("__version__")
                                or line.startswith("__author__"),
                                f,
                            ),
                        ),
                    ),
                ),
            ),
        )

    setup(
        name=package_name,
        author=__author__,
        version=__version__,
        description="Web Servers deployment module for Fabric (offregister)",
        classifiers=[
            "Development Status :: 7 - Inactive",
            "Intended Audience :: Developers",
            "Topic :: Software Development",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "License :: OSI Approved :: MIT License",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
        ],
        test_suite=package_name + ".tests",
        packages=find_packages(),
        package_dir={package_name: package_name},
        data_files=[
            (nginx_install_dir(), list(map(nginx_data, listdir(nginx_data())))),
        ],
    )
