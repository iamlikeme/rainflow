from distutils.core import setup

version = "2.1.0"

setup(
    name='rainflow',
    package_dir={"": "src"},
    py_modules=['rainflow'],
    version=version,
    description='Implementation of ASTM E1049-85 rainflow cycle counting algorythm',
    author='Piotr Janiszewski',
    author_email='i.am.like.me@gmail.com',
    url='https://github.com/iamlikeme/rainflow/',
    download_url=(
        'https://github.com/iamlikeme/rainflow/archive/v{}.tar.gz'
        .format(version)
    ),
    classifiers=[],
)
