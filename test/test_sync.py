#!/usr/bin/env python
import unittest
import logging
import sys
import os
import copy

import time
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, '..'))
from flickrsmartsync.sync import Sync
logger = logging.getLogger("flickrsmartsync")
logger.setLevel(logging.WARNING)

fakestat = os.stat(__file__)
fakeid = 45
class fakeLocal:
    files = {}
    def __init__(self):
        self.files.clear()
        self.files.update({here + os.sep + "dirname": [("file1.jpg", fakestat), ("file2.avi", fakestat)]})
    
    def build_photo_sets(self, specific_path, exts):
        return self.files
    
class fakeRemote:
    def __init__(self):
        self.photo_sets_map = {"dirname": "12345"}
        self.files = {"12345": {"file3.jpg": 23, "file4.avi": 23}}  
    def get_photo_sets(self):
        return self.photo_sets_map
    def get_custom_set_title(self, path):
        return path.split('/').pop()      
    def get_photos_in_set(self, folder, get_url=False):
        return self.files[self.photo_sets_map[folder]]  
    def upload(self, file_path, photo, folder):
        self.files[self.photo_sets_map[folder]][photo] = fakeid
    def download(self, url, path):
        fakeLocal.files.values()[0].append((os.path.basename(path), fakestat))

class syncTest(unittest.TestCase):
    maxDiff=None

    def setUp(self):
        class args:
            sync_path=here+os.sep
            custom_set=None
            ignore_images=False
            ignore_videos=False
            is_windows=False
            download="."
            sync_from="all"
        self.local = fakeLocal()
        self.remote = fakeRemote()
        self.sync = Sync(args(), self.local, self.remote)

    def tearDown(self):
        pass

    def test_upload(self):
        expected = fakeRemote().files
        for f, s in self.local.files.values()[0]:
            expected.values()[0][f] = fakeid
        self.sync.upload()
        self.assertEquals(self.remote.files, expected)

    def test_download(self):
        expected = copy.deepcopy(fakeLocal().files)
        expected.values()[0] += [(x, fakestat) for x in self.remote.files.values()[0]]
        self.sync.download()
        self.assertEquals(self.local.files, expected)

    def test_sync(self):
        expectedr = fakeRemote().files
        for f, s in self.local.files.values()[0]:
            expectedr.values()[0][f] = fakeid        
        expectedl = copy.deepcopy(fakeLocal().files)
        expectedl.values()[0] += [(x, fakestat) for x in self.remote.files.values()[0]]
        self.sync.sync()
        self.assertEquals(self.remote.files, expectedr)
        self.assertEquals(self.local.files, expectedl)
        
if __name__ == '__main__':
    logging.debug('Started test case')
    unittest.main(verbosity=2)      
