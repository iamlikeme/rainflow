from distutils.core import setup

with open("LICENSE") as f:
    LICENSE = f.read()

try:
    import pypandoc
    LONG_DESCRIPTION = pypandoc.convert("README.md", "rst")
except ImportError:
    LONG_DESCRIPTION = open("README.md").read()    

setup(name='rainflow',
      version='1.0',
      author='Piotr Janiszewski',
      author_email='i.am.like.me@gmail.com',
      url='https://github.com/iamlikeme/rainflow/',
      description='Rainflow cycle counting algorythm according to ASTM E1049-85',
      long_description=LONG_DESCRIPTION,
      license=LICENSE,
      py_modules=['rainflow'],
     )
