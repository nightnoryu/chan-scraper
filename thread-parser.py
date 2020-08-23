import argparse
import os
import sys

# Check if the module is installed
try:
    import requests
except ImportError:
    print("Please install requests module.")
    sys.exit(1)

import utils
import extractors.dvach as dvach
import extractors.fourchan as fourchan


# Parse arguments
parser = argparse.ArgumentParser(
    description="""Downloads all files, images or videos from one
    or several threads on 2ch or 4chan.""")

parser.add_argument("MODE", choices=["all", "images", "videos"],
    help="parse mode, e.g. what files to download")

parser.add_argument("URLS", nargs="*",
    help="thread urls")

parser.add_argument("-o", metavar="DIR", default=".",
    help="output directory (default: current)")

args = parser.parse_args()
mode = args.MODE
urls = args.URLS
directory = os.path.abspath(args.o)


# Parse the thread
# utils.parse_thread(url, mode, directory)
