#!/usr/bin/env python

from setuptools import setup, find_packages

__version__ = '1.0'

# To be replaced by automated build
__build__ = ''

setup(name='gusset',
      version=__version__ + __build__,
      description='Small utilities for Fabric scripts.',
      author='Location Labs',
      author_email='info@locationlabs.com',
      url='http://github.com/locationlabs/gusset',
      license='Apache2',
      packages=find_packages(exclude=['*.tests']),
      install_requires=[
          'Fabric>=1.4',
      ],
      )
