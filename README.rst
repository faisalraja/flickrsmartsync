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

    for direct python access
    $ python flickrsmartsync


Change log
==========

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