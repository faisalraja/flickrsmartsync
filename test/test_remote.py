#!/usr/bin/env python
import unittest
import logging
import sys
import os

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, '..'))
import flickrapi
from flickrsmartsync.remote import Remote, KEY, SECRET
logger = logging.getLogger("flickrsmartsync")
logger.setLevel(logging.WARNING)

class authedRemote(Remote):
    def auth_api(self):
        token = "72157645636119732-71cd968268ffd2e5"
        self.api = flickrapi.FlickrAPI(KEY, SECRET, username="rqpmbdqm24", token=token)
        return token

class remoteTest(unittest.TestCase):

    def setUp(self):
        class args:
            username=None
            sync_path=here+os.sep
            custom_set=None
            update_custom_set=None
            custom_set_builder=None
            is_windows=False
            download=None
        self.remote = authedRemote(args())
        self.deletePhotoset = None
        self.deleteFile = None
        self.deletePhoto = None

    def tearDown(self):
        if self.deletePhotoset:
            try:
                self.remote.api.photosets_delete(photoset_id=self.deletePhotoset)
            except:
                pass
        if self.deletePhoto:
            try:
                self.remote.api.photos_delete(photo_id=self.deletePhoto)
            except:
                pass
        if self.deleteFile:
            os.remove(self.deleteFile)

    def test_list_sets(self):
        self.assertEquals(self.remote.get_photo_sets(), {'Gradient test images': u'72157645524834044'})

    def test_list_photos(self):
        self.assertEquals(self.remote.get_photos_in_set('Gradient test images'),{'Black gradient (reasonable size).jpg': u'14491535316'})

    def test_add_to_set(self):
        self.remote.add_to_photo_set(14524802935, 'Stuff2')
        self.deletePhotoset = self.remote.get_photo_sets()['Stuff2']
        self.assertEquals(len(self.remote.get_photos_in_set('Stuff2')),1)
        self.remote.add_to_photo_set(14491535316, 'Stuff2')
        self.assertEquals(len(self.remote.get_photos_in_set('Stuff2')),2)

    def test_addPhoto(self):
        self.deletePhoto = self.remote.upload(here+'/images/new_gradient.jpg', 'new_gradient.jpg', 'images')
        self.deletePhotoset = self.remote.get_photo_sets()['images']
        self.assertEquals(len(self.remote.get_photos_in_set('images')),1)

    def test_customSet(self):
        self.remote.cmd_args.custom_set = ".*im(.*)"
        self.deletePhoto = self.remote.upload(here+'/images/new_gradient.jpg', 'new_gradient.jpg', 'images')
        self.deletePhotoset = self.remote.get_photo_sets()['images']
        self.assertEquals(self.remote.api.photosets_getInfo(photoset_id=self.deletePhotoset).find("photoset").find("title").text, "ages")
        self.remote.cmd_args.update_custom_set = True
        self.remote.cmd_args.custom_set = ".*i(.*)"
        self.remote.update_photo_sets_map()
        self.assertEquals(self.remote.api.photosets_getInfo(photoset_id=self.deletePhotoset).find("photoset").find("title").text, "mages")

    def test_download(self):
        images = self.remote.get_photos_in_set('Gradient test images', get_url=True)
        self.assertEquals(len(images), 1)
        self.deleteFile = here+os.sep+"tmp.jpg"
        self.remote.download(images.values()[0], self.deleteFile)
        self.assertEquals(os.path.isfile(self.deleteFile), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
