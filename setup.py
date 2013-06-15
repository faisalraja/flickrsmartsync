#! /usr/bin/env python

from setuptools import setup, find_packages
import sys
import os

version = '0.1.7'


def main():
    setup(name='flickrsmartsync',
          version=version,
          description="Sync/backup your photos to flickr easily",
          long_description=open('README.md').read(),
          classifiers=[],
          keywords='flickr backup photo sync',
          author='Faisal Raja',
          author_email='support@altlimit.com',
          url='https://github.com/faisalraja/flickrsmartsync',
          license='MIT',
          packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
          include_package_data=True,
          zip_safe=False,
          install_requires=[],
          entry_points={
              "console_scripts": ['flickrsmartsync = flickrsmartsync:main'],
          },
          )

if __name__ == '__main__':
    main()
