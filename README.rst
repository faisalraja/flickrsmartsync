flickrsmartsync - Sync/backup your photos to flickr easily
**********************************************************

flickrsmartsync is a tool you can use to easily sync up or down your
photos in a drive/folder to flickr since now it has a free 1TB storage
you can probably sync all your photo collection.


Install
=======

Simply run the following::

    $ python setup.py install

or `PyPi`_::

    $ pip install flickrsmartsync


Example Usage
==============

Both run from source and command line have same parameters::

    start uploading all photos/videos under that folder
    $ flickrsmartsync
    ignore videos for others use --help
    $ flickrsmartsync --ignore-videos

    start downloading all photos on flickr to that folder
    $ flickrsmartsync --download .
    
    start downloading all paths starting with that path
    $ flickrsmartsync --download 2008/2008-01-01

    Generate custom set titles from YEAR/MONTH/DAY folder hierarchy:
    $  flickrsmartsync --custom-set='(?:.*)((?:19|20)\d{2})/(\d{2})/(\d{2})' --custom-set-builder '{0}-{1}-{2}'

    for direct python access
    $ python flickrsmartsync


Change log
==========

0.2.02 (2017-02-11)
 * added --fix-missing-description option (thanks jruusu)
 * added --dry-run option (thanks jruusu)

0.2.01 (2015-02-17)
 * added --custom-set-debug for testing custom sets output
 * added --ignore-ext comma separated extensions to ignore

0.2.00 (2015-02-15)
 * Refactor code into sync, local and remote classes
 * Add test cases that do a limited test of each class in isolation
 * Add a sync-from=all command line option that allows a download of any remote file not on local, and upload of any local file not on remote as discussed in #22
 * Add retries on uploads and downloads
 * Add a file extension on download if one doesn't exist
 * Incorporate pull request #32 which fixes #31 with slight changes
 * Thanks thomascobb

0.1.18 (2014-11-14)
 * browser-less authentication

0.1.17 (2014-08-12)
 * allow filtering files to upload by IPTC keyword (thanks ricardokirkner)
 * updated flickrapi 1.4.4

0.1.16 (2014-06-30)
 * flickr api changes use https

0.1.15 (2014-05-30)
 * monitor folder support (--monitor)

0.1.14.3 (2014-05-18)
 * encoding bug

0.1.14.2 (2014-04-15)
 * send script output to syslog for headless convience (thanks dahlb)

0.1.14 (2014-02-25)
 * added --starts-with param
 * added --version param
 * bug fix not uploading files properly

0.1.12 (2014-02-15)
 * added custom set title
 * character encoding bugs
 * skip failures

0.1.11 (2013-07-09)

 * added mts video
 * added folder utf8 encoding to avoid dups
 * added sorting for each folders

0.1.10 (2013-07-07)

 * sorted photo sets
 * ignore files > 1gb

0.1.9 (2013-06-28)

 * added --sync-path param

0.1.8 (2013-06-25)

 * ignore hidden folders/folders
 * added video support
 * added new params for skipping video/images

0.1.7 (2013-06-15)

 * added run from source

0.1 (2013-06-13)


Links
=====
* `github.com`_ - source code
* `altlimit.com`_ - website
* `blog post`_ - blog post

.. _github.com: https://github.com/faisalraja/flickrsmartsync
.. _PyPi: https://pypi.python.org/pypi/flickrsmartsync
.. _altlimit.com: http://www.altlimit.com
.. _blog post: http://blog.altlimit.com/2013/05/backupsync-your-photos-to-flickr-script.html
