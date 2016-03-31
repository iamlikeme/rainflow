from distutils.core import setup

LICENSE = open("LICENSE").read()
LONG_DESCRIPTION = open("README.md").read()    

setup(name='rainflow',
      version='1.0.1',
      author='Piotr Janiszewski',
      author_email='i.am.like.me@gmail.com',
      url='https://github.com/iamlikeme/rainflow/',
      description='Rainflow cycle counting algorythm according to ASTM E1049-85',
      long_description=LONG_DESCRIPTION,
      license=LICENSE,
      py_modules=['rainflow'],
     )
