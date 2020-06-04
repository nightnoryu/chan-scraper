import argparse
import os

import requests


def get_api_url(url):
	'''Returns an API url (html -> json)'''
    array = url.split('.')
    api_url = '.'.join(array[:-1])
    return api_url + '.json'


def is_image(ext):
    return (ext == 'jpg' or ext == 'jpeg' or
            ext == 'png' or ext =='gif')


def is_video(ext):
    return ext == 'webm' or ext == 'mp4'


def count_files(posts, mode='all'):
    n = 0
    for post in posts:
        for fname in post['fnames']:
            ext = fname['name'].split('.')[-1]
            if mode == 'images':
                if is_image(ext):
                    n += 1
                else:
                    continue
            elif mode == 'videos':
                if is_video(ext):
                    n += 1
                else:
                    continue
            elif mode == 'all':
                n += 1
    return n


# Parse arguments
parser = argparse.ArgumentParser(
	description='''Downloads all files, images or videos from the thread on 2ch.hk.''')

parser.add_argument('MODE', choices=['all', 'images', 'videos'],
	help='parse mode, e.g. what files to download')

parser.add_argument('URL',
	help='thread url')

args = parser.parse_args()
mode = args.MODE
url = args.URL


# Get the thread's JSON
api_url = get_api_url(url)
response = requests.get(api_url)
# Parse it down n' hard
res_json = response.json()
posts = res_json['threads'][0]['posts']


# Ask user
print('Files will be saved in the current directory.')
choice = input('Proceed (Y/n)? ')
if not (choice == 'y' or choice == 'Y' or choice == ''):
	print('As you wish...')
	sys.exit(0)
