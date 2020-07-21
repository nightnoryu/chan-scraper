import argparse
import os
import sys

import requests

import utils
import extractors.dvach as dvach


# Parse arguments
parser = argparse.ArgumentParser(
    description="""Downloads all files, images or videos from the
    thread on 2ch.hk.""")

parser.add_argument("MODE", choices=["all", "images", "videos"],
    help="parse mode, e.g. what files to download")

parser.add_argument("URL",
    help="thread url")

parser.add_argument("-o", metavar="DIR", default=".",
    help="output directory (default: current)")

args = parser.parse_args()
mode = args.MODE
url = args.URL
directory = os.path.abspath(args.o)


try:
    # Get all the files' URLs
    file_list = dvach.get_files_urls_names(url)
    # Count the files
    amount = utils.count_files(file_list, mode)
except Exception as ex:
    # Handle requests exceptions
    print("Request error: {}".format(ex))
    print("Download failed, exiting.")
    sys.exit(1)


# Ask user
print("{} files will be saved in the '{}' directory.".format(amount,
    directory))
choice = input("Proceed (Y/n)? ")
if not (choice.lower() in ["y", ""]):
    print("As you wish...")
    sys.exit(0)


# Check the output directory
if not os.path.isdir(directory):
    print("\nHmm, '{}' directory doesn't seem to exist...".format(directory))
    print("Nevermind, I'll just create one.")
    os.mkdir(directory)


# Actual downloading is happening here
print("\nDownloading...")
# Posts loop
n = 1
for file_url, file_name in file_list:
    ext = utils.get_extension(file_url)
    # Save the files according to the mode
    if ((mode == "images" and utils.is_image(ext)) or
        (mode == "videos" and utils.is_video(ext)) or
        (mode == "all")):
        utils.save_file(file_url,
            directory,
            file_name)
        print("{:>3}/{} - {}".format(n, amount, file_name))
        n += 1
