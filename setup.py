from setuptools import setup, find_packages
from os import path, listdir
from functools import partial
from ast import parse
from distutils.sysconfig import get_python_lib

if __name__ == "__main__":
    package_name = "offregister_web_servers"

    f_for = partial(path.join, path.dirname(__file__), package_name)
    d_for = partial(path.join, get_python_lib(), package_name)

    nginx_data = partial(path.join, f_for("nginx", "data"))
    nginx_install_dir = partial(path.join, d_for("nginx", "data"))

    get_vals = lambda var0, var1: list(
        map(
            lambda buf: next([e.value.s for e in parse(buf).body]),
            [line for line in f if line.startswith(var0) or line.startswith(var1)],
        )
    )

    with open(path.join(package_name, "__init__.py")) as f:
        __author__, __version__ = get_vals("__version__", "__author__")

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
