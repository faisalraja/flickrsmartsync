#!/usr/bin/env python
import unittest
import logging
import sys
import os
import flickrapi
import time
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, '..'))
from flickrsmartsync.sync import Sync
logger = logging.getLogger("flickrsmartsync")
logger.setLevel(logging.WARNING)

fakestat = os.stat(__file__)
class fakeLocal:
    def __init__(self):
        self.files = {here + os.sep + "dirname": [("file1.jpg", fakestat), ("file2.avi", fakestat)]}
    
    def build_photo_sets(self, specific_path, exts):
        return self.files
    
class fakeRemote:
    def __init__(self):
        self.photo_sets_map = {"dirname": "12345"}
        self.files = {"12345": ["file3.jpg", "file4.avi"]}  
    def get_custom_set_title(self, path):
        return path.split('/').pop()      
    def get_photos_in_set(self, folder, get_url=False):
        return self.files[self.photo_sets_map[folder]]  
    def upload(self, file_path, photo, folder):
        self.files[self.photo_sets_map[folder]].append(photo)

class syncTest(unittest.TestCase):

    def setUp(self):
        class args:
            sync_path=here+os.sep
            custom_set=None
            ignore_images=False
            ignore_videos=False
            is_windows=False
        self.local = fakeLocal()
        self.remote = fakeRemote()
        self.sync = Sync(args(), self.local, self.remote)

    def tearDown(self):
        pass

    def test_upload(self):
        expected = fakeRemote().files
        expected.values()[0] += [x[0] for x in self.local.files.values()[0]]
        self.sync.upload()
        self.assertEquals(self.remote.files, expected)

#    def test_download(self):
#        expected = fakeLocal().files
#        expected.values()[0] += [x[0] for x in self.local.files.values()[0]]
#        self.sync.upload()
#        self.assertEquals(self.remote.files, expected)

if __name__ == '__main__':
    logging.debug('Started test case')
    unittest.main(verbosity=2)      
