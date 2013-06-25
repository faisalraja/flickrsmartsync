#
import HTMLParser
import json
import os
import urllib
import argparse
import flickrapi

__author__ = 'faisal'

EXT_IMAGE = ('jpg', 'png', 'jpeg', 'gif', 'bmp')
EXT_VIDEO = ('avi', 'wmv', 'mov', 'mp4', '3gp', 'ogg', 'ogv')

def start_sync(sync_path, cmd_args):
    is_windows = os.name == 'nt'
    is_download = cmd_args.download

    # Put your API & SECRET keys here
    KEY = 'f7da21662566bc773c7c750ddf7030f7'
    SECRET = 'c329cdaf44c6d3f3'

    # Common arguments
    args = {'format': 'json', 'nojsoncallback': 1}
    api = flickrapi.FlickrAPI(KEY, SECRET)
    # api.token.path = 'flickr.token.txt'

    # Ask for permission
    (token, frob) = api.get_token_part_one(perms='write')

    if not token:
        raw_input("Please authorized this app then hit enter:")

    try:
        token = api.get_token_part_two((token, frob))
    except:
        print 'Please authorized to use'
        exit(0)

    args.update({'auth_token': token})

    # Build your local photo sets
    photo_sets = {}
    skips_root = []
    for r, dirs, files in os.walk(sync_path):
        files = [f for f in files if not f.startswith('.')]
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if not file.startswith('.'):
                ext = file.lower().split('.').pop()
                if ext in EXT_IMAGE or \
                   ext in EXT_VIDEO:

                    if r == sync_path:
                        skips_root.append(file)
                    else:
                        photo_sets.setdefault(r, [])
                        photo_sets[r].append(file)

    if skips_root:
        print 'To avoid disorganization on flickr sets root photos are not synced, skipped these photos:', skips_root
        print 'Try to sync at top most level of your photos directory'

    # Get your photosets online and map it to your local
    html_parser = HTMLParser.HTMLParser()
    photosets_args = args.copy()
    page = 1
    photo_sets_map = {}
    while True:
        print 'Getting photosets page %s' % page
        photosets_args.update({'page': page, 'per_page': 500})
        sets = json.loads(api.photosets_getList(**photosets_args))
        page += 1
        if not sets['photosets']['photoset']:
            break

        for set in sets['photosets']['photoset']:
            # Make sure it's the one from backup format
            desc = html_parser.unescape(set['description']['_content'])
            if desc.endswith(set['title']['_content']):
                photo_sets_map[desc] = set['id']

    print 'Found %s photo sets' % len(photo_sets_map)

    # For adding photo to set
    def add_to_photo_set(photo_id, folder):
        # If photoset not found in online map create it else add photo to it
        # Always upload unix style
        if is_windows:
            folder = folder.replace(os.sep, '/')

        if folder not in photo_sets_map:
            photosets_args = args.copy()
            photosets_args.update({'primary_photo_id': photo_id,
                                   'title': folder.split('/').pop(),
                                   'description': folder})
            set = json.loads(api.photosets_create(**photosets_args))
            photo_sets_map[folder] = set['photoset']['id']
            print 'Created set [%s] and added photo' % folder
        else:
            photosets_args = args.copy()
            photosets_args.update({'photoset_id': photo_sets_map.get(folder), 'photo_id': photo_id})
            result = json.loads(api.photosets_addPhoto(**photosets_args))
            if result.get('stat') == 'ok':
                print 'Success'
            else:
                print result

    # Get photos in a set
    def get_photos_in_set(folder):
        photos = {}
        # Always upload unix style
        if is_windows:
            folder = folder.replace(os.sep, '/')

        if folder in photo_sets_map:
            photoset_args = args.copy()
            page = 1
            while True:
                photoset_args.update({'photoset_id': photo_sets_map[folder], 'page': page})
                if is_download:
                    photoset_args['extras'] = 'url_o,media'
                page += 1
                photos_in_set = json.loads(api.photosets_getPhotos(**photoset_args))
                if photos_in_set['stat'] != 'ok':
                    break

                for photo in photos_in_set['photoset']['photo']:

                    if is_download and photo.get('media') == 'video':
                        # photo_args = args.copy()
                        # photo_args['photo_id'] = photo['id']
                        # sizes = json.loads(api.photos_getSizes(**photo_args))
                        # if sizes['stat'] != 'ok':
                        #     continue
                        #
                        # original = filter(lambda s: s['label'].startswith('Site') and s['media'] == 'video', sizes['sizes']['size'])
                        # if original:
                        #     photos[photo['title']] = original.pop()['source'].replace('/site/', '/orig/')
                        #     print photos
                        # Skipts download video for now since it doesn't work
                        continue
                    else:
                        photos[photo['title']] = photo['url_o'] if is_download else photo['id']

        return photos

    # If download mode lets skip upload but you can also modify this to your needs
    if is_download:
        # Download to corresponding paths
        os.chdir(sync_path)

        for photo_set in photo_sets_map:
            if photo_set and is_download == '.' or is_download != '.' and photo_set.startswith(is_download):
                folder = photo_set.replace(sync_path, '')
                print 'Getting photos in set [%s]' % folder
                photos = get_photos_in_set(folder)
                # If Uploaded on unix and downloading on windows & vice versa
                if is_windows:
                    folder = folder.replace('/', os.sep)

                if not os.path.isdir(folder):
                    os.makedirs(folder)

                for photo in photos:
                    # Adds skips
                    if cmd_args.ignore_images and photo.split('.').pop().lower() in EXT_IMAGE:
                        continue
                    elif cmd_args.ignore_videos and photo.split('.').pop().lower() in EXT_VIDEO:
                        continue

                    path = os.path.join(folder, photo)
                    if os.path.exists(path):
                        print 'Skipped [%s] already downloaded' % path
                    else:
                        print 'Downloading photo [%s]' % path
                        urllib.urlretrieve(photos[photo], os.path.join(sync_path, path))
    else:
        # Loop through all local photo set map and
        # upload photos that does not exists in online map
        for photo_set in photo_sets:
            folder = photo_set.replace(sync_path, '')
            print 'Getting photos in set [%s]' % folder
            photos = get_photos_in_set(folder)
            print 'Found %s photos' % len(photos)

            for photo in photo_sets[photo_set]:
                # Adds skips
                if cmd_args.ignore_images and photo.split('.').pop().lower() in EXT_IMAGE:
                    continue
                elif cmd_args.ignore_videos and photo.split('.').pop().lower() in EXT_VIDEO:
                    continue

                if photo in photos or is_windows and photo.replace(os.sep, '/') in photos:
                    print 'Skipped [%s] already exists in set [%s]' % (photo, folder)
                else:
                    print 'Uploading [%s] to set [%s]' % (photo, folder)
                    upload_args = {'auth_token': token, 'title': photo, 'hidden': 1, 'is_public': 0, 'is_friend': 0, 'is_family': 0}
                    try:
                        upload = api.upload(os.path.join(photo_set, photo), None, **upload_args)
                        photo_id = upload.find('photoid').text
                        add_to_photo_set(photo_id, folder)
                        photos[photo] = photo_id
                    except flickrapi.FlickrError as e:
                        print e.message

    print 'All Synced'


def main():
    parser = argparse.ArgumentParser(description='Sync current folder to your flickr account.')
    parser.add_argument('--download', type=str, help='download the photos from flickr specify a path or . for all')
    parser.add_argument('--ignore-videos', action='store_true', help='ignore video files')
    parser.add_argument('--ignore-images', action='store_true', help='ignore image files')

    args = parser.parse_args()
    start_sync(os.getcwd() + os.sep, args)