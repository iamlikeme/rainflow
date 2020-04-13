from setuptools import setup
import os


def load_version(path):
    with open(path, "rb") as f:
        lines = f.read().decode("utf-8").splitlines()

    for line in lines:
        d = {}
        try:
            exec(line, d)
            return d["__version__"]
        except KeyError:
            continue
        except Exception:
            continue
    raise Exception("__version__ not found in {}".format(path))


this_dir = os.path.dirname(__file__)

version = load_version(path=os.path.join(this_dir, "src", "rainflow.py"))

with open(os.path.join(this_dir, "README.md"), "rb") as fo:
    long_description = fo.read().decode("utf8")


setup(
    name='rainflow',
    package_dir={"": "src"},
    py_modules=['rainflow'],
    version=version,
    description='Implementation of ASTM E1049-85 rainflow cycle counting algorithm',
    extras_require={"dev": ["pytest ~= 4.6"]},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Piotr Janiszewski',
    author_email='i.am.like.me@gmail.com',
    url='https://github.com/iamlikeme/rainflow/',
    license="MIT",
    download_url=(
        'https://github.com/iamlikeme/rainflow/archive/v{}.tar.gz'
        .format(version)
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
