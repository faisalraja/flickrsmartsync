#
# -*- coding: utf-8 -*-
import argparse
import os
import logging
from logging.handlers import SysLogHandler
from sync import Sync
from local import Local
from remote import Remote

__author__ = 'faisal'
# todo get from setup.cfg
version = '0.2.02'

logging.basicConfig()
logger = logging.getLogger("flickrsmartsync")
hdlr = SysLogHandler()
formatter = logging.Formatter('flickrsmartsync %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='Sync current folder to your flickr account.')
    parser.add_argument('--monitor', action='store_true', 
                        help='starts a daemon after sync for monitoring')
    parser.add_argument('--starts-with', type=str, 
                        help='only sync that path starts with this text, e.g. "2015/06"')
    parser.add_argument('--download', type=str, 
                        help='download the photos from flickr, specify a path or . for all')
    parser.add_argument('--dry-run', action='store_true',
                        help='do not download or upload anything')
    parser.add_argument('--ignore-videos', action='store_true', 
                        help='ignore video files')
    parser.add_argument('--ignore-images', action='store_true', 
                        help='ignore image files')
    parser.add_argument('--ignore-ext', type=str, 
                        help='comma separated list of extensions to ignore, e.g. "jpg,png"')
    parser.add_argument('--fix-missing-description', action='store_true',
                        help='given a missing set description, replaces it with set title')
    parser.add_argument('--version', action='store_true', 
                        help='output current version: ' + version)
    parser.add_argument('--sync-path', type=str, default=os.getcwd(),
                        help='specify the sync folder (default is current dir)')
    parser.add_argument('--sync-from', type=str, 
                        help='Only supported value: "all". Uploads anything that isn\'t on flickr, and download anything that isn\'t on the local filesystem')
    parser.add_argument('--custom-set', type=str, 
                        help='customize your set name from path with regex, e.g. "(.*)/(.*)"')
    parser.add_argument('--custom-set-builder', type=str, 
                        help='build your custom set title, e.g. "{0} {1}" to join the first two groups (default merges groups with hyphen)')
    parser.add_argument('--update-custom-set', action='store_true', 
                        help='updates your set title from custom-set (and custom-set-builder, if given)')
    parser.add_argument('--custom-set-debug', action='store_true', 
                        help='for testing your custom sets, asks for confirmation when creating an album on flickr')
    parser.add_argument('--username', type=str, 
                        help='token username')  # token username argument for api
    parser.add_argument('--keyword', action='append', type=str, 
                        help='only upload files matching this keyword')

    args = parser.parse_args()

    if args.version:
        logger.info(version)
        exit()

    # validate args
    args.is_windows = os.name == 'nt'
    args.sync_path = args.sync_path.rstrip(os.sep) + os.sep
    if not os.path.exists(args.sync_path):
        logger.error('Sync path does not exists')
        exit(0)

    local = Local(args)
    remote = Remote(args)
    sync = Sync(args, local, remote)
    sync.start_sync()

