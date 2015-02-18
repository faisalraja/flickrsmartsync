#! /usr/bin/env python

from setuptools import setup, find_packages
import sys
import os

VERSION = '0.2.01'


def main():
    setup(name='flickrsmartsync',
          version=VERSION,
          description="Sync/backup your photos to flickr easily",
          long_description=open('README.rst').read(),
          classifiers=[
              'Development Status :: 3 - Alpha',
              'Environment :: Console',
              'Programming Language :: Python',
              'License :: OSI Approved :: MIT License'
          ],
          keywords='flickr backup photo sync',
          author='Faisal Raja',
          author_email='support@altlimit.com',
          url='https://github.com/faisalraja/flickrsmartsync',
          license='MIT',
          packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
          include_package_data=True,
          zip_safe=False,
          install_requires=['watchdog', 'IPTCInfo'],
          entry_points={
              "console_scripts": ['flickrsmartsync = flickrsmartsync:main'],
          },
          )

if __name__ == '__main__':
    main()
