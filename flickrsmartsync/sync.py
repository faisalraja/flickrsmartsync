import os
import logging
logger = logging.getLogger("flickrsmartsync")

EXT_IMAGE = ('jpg', 'png', 'jpeg', 'gif', 'bmp')
EXT_VIDEO = ('avi', 'wmv', 'mov', 'mp4', '3gp', 'ogg', 'ogv', 'mts')

class Sync(object):
    def __init__(self, cmd_args, local, remote):
        self.cmd_args = cmd_args
        # Create local and remote objects
        self.local = local
        self.remote = remote

    def start_sync(self):
        # Do the appropriate one time sync
        if self.cmd_args.download:
            self.download()
        elif self.cmd_args.sync:
            self.sync()
        else:
            self.upload()
            logger.info('Upload done')
            if self.cmd_args.monitor:
                self.local.watch_for_changes(self.upload)
                self.local.wait_for_quit()

    def download(self):
        # Download to corresponding paths
        for photo_set in self.remote.get_photo_sets():
            if photo_set and (self.cmd_args.download == '.' or photo_set.startswith(self.cmd_args.download)):
                folder = os.path.join(self.cmd_args.sync_path, photo_set)
                logger.info('Getting photos in set [%s]' % photo_set)
                photos = self.remote.get_photos_in_set(photo_set, get_url=True)
                # If Uploaded on unix and downloading on windows & vice versa
                if self.cmd_args.is_windows:
                    folder = folder.replace('/', os.sep)

                for photo in photos:
                    # Adds skips
                    if self.cmd_args.ignore_images and photo.split('.').pop().lower() in EXT_IMAGE:
                        continue
                    elif self.cmd_args.ignore_videos and photo.split('.').pop().lower() in EXT_VIDEO:
                        continue

                    path = os.path.join(photo_set, photo)
                    if os.path.exists(path):
                        logger.info('Skipped [%s] already downloaded' % path)
                    else:
                        logger.info('Downloading photo [%s]' % path)
                        self.remote.download(photos[photo], os.path.join(self.cmd_args.sync_path, path))

    def upload(self, specific_path=None):
        if specific_path == None:
            only_dir = self.cmd_args.sync_path
        else:
            only_dir = os.path.dirname(specific_path)
        photo_sets = self.local.build_photo_sets(only_dir, EXT_IMAGE + EXT_VIDEO)
        logger.info('Found %s photo sets' % len(photo_sets))

        if specific_path == None:
            # Show custom set titles
            if self.cmd_args.custom_set:
                for photo_set in photo_sets:
                    logger.info('Set Title: [%s]  Path: [%s]' % (self.remote.get_custom_set_title(photo_set), photo_set))

                if raw_input('Is this your expected custom set titles (y/n):') != 'y':
                    exit(0)

        # Loop through all local photo set map and
        # upload photos that does not exists in online map
        for photo_set in sorted(photo_sets):
            folder = photo_set.replace(self.cmd_args.sync_path, '')
            display_title = self.remote.get_custom_set_title(photo_set)
            logger.info('Getting photos in set [%s]' % display_title)
            photos = self.remote.get_photos_in_set(folder)
            logger.info('Found %s photos' % len(photos))

            for photo, file_stat in sorted(photo_sets[photo_set]):
                # Adds skips
                if self.cmd_args.ignore_images and photo.split('.').pop().lower() in EXT_IMAGE:
                    continue
                elif self.cmd_args.ignore_videos and photo.split('.').pop().lower() in EXT_VIDEO:
                    continue

                if photo in photos or self.cmd_args.is_windows and photo.replace(os.sep, '/') in photos:
                    logger.info('Skipped [%s] already exists in set [%s]' % (photo, display_title))
                else:
                    logger.info('Uploading [%s] to set [%s]' % (photo, display_title))
                    if file_stat.st_size >= 1073741824:
                        logger.error('Skipped [%s] over size limit' % photo)
                        continue
                    file_path = os.path.join(photo_set, photo)                        
                    photo_id = self.remote.upload(file_path, photo, folder)
                    if photo_id:
                        photos[photo] = photo_id



