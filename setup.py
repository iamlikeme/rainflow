from setuptools import setup
import os

this_dir = os.path.dirname(__file__)

with open(os.path.join(this_dir, "README.md"), "rb") as fo:
    long_description = fo.read().decode("utf8")


setup(
    name='rainflow',
    package_dir={"": "src"},
    py_modules=['rainflow'],
    description='Implementation of ASTM E1049-85 rainflow cycle counting algorithm',
    install_requires=["importlib_metadata ; python_version < '3.8'"],
    extras_require={"dev": ["pytest ~= 4.6"]},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Piotr Janiszewski',
    url='https://github.com/iamlikeme/rainflow/',
    license="MIT",
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
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
