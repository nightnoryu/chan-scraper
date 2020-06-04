import argparse
import os

import requests


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


# Download the content
