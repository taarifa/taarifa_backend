try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as f:
    install_requires = f.readlines()

# Get the package version without importing anyting from pyop2
execfile('taarifa_backend/version.py')
setup(name='Taarifa Backend',
      version=__version__,  # noqa: pulled from taarifa_backend/version.py
      description='Prototype of a Taarifa backend',
      author='The Taarifa Organisation',
      author_email='taarifadev@gmail.com',
      url='http://taarifa.org',
      download_url='https://github.com/taarifa/taarifa_backend',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ],
      setup_requires=['flake8'],
      install_requires=install_requires,
      packages=['taarifa_backend'])
