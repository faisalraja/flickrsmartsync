from iptcinfo import IPTCInfo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
import os

logger = logging.getLogger("flickrsmartsync")


class Local(object):
    def __init__(self, cmd_args):
        self.cmd_args = cmd_args

    def build_photo_sets(self, path, extensions):
        # Build your local photo sets
        photo_sets = {}
        skips_root = []
        keywords = set(self.cmd_args.keyword) if self.cmd_args.keyword else ()

        for r, dirs, files in os.walk(path, followlinks=True):

            if self.cmd_args.starts_with and not r.startswith('{}{}'.format(self.cmd_args.sync_path, self.cmd_args.starts_with)):
                continue

            files = [f for f in files if not f.startswith('.')]
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if not file.startswith('.'):
                    ext = file.lower().split('.').pop()
                    if ext in extensions:
                        if r == self.cmd_args.sync_path:
                            skips_root.append(file)
                        else:
                            # filter by keywords
                            if keywords:
                                file_path = os.path.join(r, file)
                                info = IPTCInfo(file_path, force=True)
                                matches = keywords.intersection(info.keywords)
                                if not matches:
                                    # no matching keyword(s) found, skip file
                                    logger.info('Skipped [%s] does not match any keyword %s' % (file, list(keywords)))
                                    continue

                            photo_sets.setdefault(r, [])
                            file_path = os.path.join(r, file)
                            file_stat = os.stat(file_path)
                            photo_sets[r].append((file, file_stat))

        if skips_root:
            logger.warn('To avoid disorganization on flickr sets root photos are not synced, skipped these photos: %s' % skips_root)
            logger.warn('Try to sync at top most level of your photos directory')
        return photo_sets

    def watch_for_changes(self, upload_func):
        logger.info('Monitoring [{}]'.format(self.cmd_args.sync_path))
        event_handler = WatchEventHandler(self.cmd_args.sync_path, upload_func)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.cmd_args.sync_path, recursive=True)
        self.observer.start()

    def wait_for_quit(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class WatchEventHandler(FileSystemEventHandler):
    sync_path = None

    def __init__(self, sync_path, upload_func):
        self.sync_path = sync_path.rstrip(os.sep)
        self.upload_func = upload_func

    def on_created(self, event):
        super(WatchEventHandler, self).on_created(event)

        if not event.is_directory:
            self.upload_func(event.src_path)

    def on_moved(self, event):
        super(WatchEventHandler, self).on_moved(event)

        if not event.is_directory and os.path.dirname(event.dest_path).replace(self.sync_path, ''):
            self.upload_func(event.dest_path)
