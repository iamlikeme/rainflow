from distutils.core import setup
import os

version = "2.1.1"
this_dir = os.path.dirname(__file__)

with open(os.path.join(this_dir, "README.md"), "rb") as fo:
    long_description = fo.read().decode("utf8")

setup(
    name='rainflow',
    package_dir={"": "src"},
    py_modules=['rainflow'],
    version=version,
    description='Implementation of ASTM E1049-85 rainflow cycle counting algorythm',
    long_description=long_description,
    author='Piotr Janiszewski',
    author_email='i.am.like.me@gmail.com',
    url='https://github.com/iamlikeme/rainflow/',
    download_url=(
        'https://github.com/iamlikeme/rainflow/archive/v{}.tar.gz'
        .format(version)
    ),
    classifiers=[],
)
