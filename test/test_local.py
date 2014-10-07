#!/usr/bin/env python
import unittest
import logging
import sys
import os
import time
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, '..'))
from flickrsmartsync.local import Local

logger = logging.getLogger("flickrsmartsync")
logger.setLevel(logging.WARNING)

class localTest(unittest.TestCase):

    def setUp(self):
        class args:
            sync_path=here+os.sep
            starts_with=None
            keyword=None
        self.local = Local(args())
        self.watch_path = None

    def tearDown(self):
        if self.watch_path:
            os.remove(self.watch_path)

    def test_list_files(self):
        ps = self.local.build_photo_sets(here, ('jpg',))
        self.assertEquals(ps, {here+os.sep+'images': [('new_gradient.jpg', os.stat(here+os.sep+'images'+os.sep+'new_gradient.jpg'))]})

    def test_starts_with(self):
        self.local.cmd_args.starts_with = 'images'
        self.test_list_files()

    def upload_func(self, path):
        self.watch_path=path

    def test_monitor(self):
        self.local.watch_for_changes(self.upload_func)
        p = os.sep.join((here,"images","new.jpg"))
        open(p, "w").write("test")
        time.sleep(1)
        self.assertEquals(self.watch_path, p)


if __name__ == '__main__':
    logging.debug('Started test case')
    unittest.main(verbosity=2)        
