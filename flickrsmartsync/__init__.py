#
import HTMLParser
import json
import os
import urllib

import argparse

import flickrapi


__author__ = 'faisal'


def start_sync(sync_path, is_download):

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
    for r, d, f in os.walk(sync_path):
        for file in f:
            if file.lower().split('.').pop() in ('jpg', 'png', 'jpeg', 'gif', 'bmp'):
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
        if '\'' in folder:
            folder = folder.replace('\'', '/')

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
        if '\'' in folder:
            folder = folder.replace('\'', '/')

        if folder in photo_sets_map:
            photoset_args = args.copy()
            page = 1
            while True:
                photoset_args.update({'photoset_id': photo_sets_map[folder], 'page': page})
                if is_download:
                    photoset_args['extras'] = 'url_o'
                page += 1
                photos_in_set = json.loads(api.photosets_getPhotos(**photoset_args))
                if photos_in_set['stat'] != 'ok':
                    break

                for photo in photos_in_set['photoset']['photo']:
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
                if '/' in folder and os.sep != '/':
                    folder = folder.replace('/', os.sep)
                elif '\'' in folder and os.sep != '\'':
                    folder = folder.replace('\'', os.sep)

                if not os.path.isdir(folder):
                    os.makedirs(folder)

                for photo in photos:
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
                if photo in photos:
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

    args = parser.parse_args()
    start_sync(os.getcwd() + os.sep, args.download)