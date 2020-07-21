import argparse
import os
import sys

import requests

import utils
import extractors.dvach as dvach
import extractors.fourchan as fourchan


def what_board_is_this(url):
    """Returns a name of the board depending on the thread URL"""
    if url.startswith("https://2ch."):
        return "2ch"
    elif (url.startswith("https://boards.4channel.org") or
          url.startswith("https://boards.4chan.org")):
        return "4chan"


# Parse arguments
parser = argparse.ArgumentParser(
    description="""Downloads all files, images or videos from the
    thread on 2ch or 4chan.""")

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


# Select the extractor
extractor = None
if what_board_is_this(url) == "2ch":
    extractor = dvach
elif what_board_is_this(url) == "4chan":
    extractor = fourchan


try:
    # Get all the files' URLs
    file_list = extractor.get_files_urls_names(url)
    # Count the files
    amount = utils.count_files(file_list, mode)
except Exception as ex:
    # Handle requests exceptions
    print("Request error: {}".format(ex))
    print("Download failed, exiting.")
    sys.exit(1)


# Check if there's any files
if amount == 0:
    print("There are no files in this thread: {}".format(url))
    sys.exit(0)

# Ask user
print("{} {} will be saved in the '{}' directory.".format(amount,
    "file" if amount == 1 else "files",
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
        # Save the file
        utils.save_file(file_url, directory, file_name)
        # Log the action
        print("{:>3}/{} - {}".format(n, amount, file_name))
        # Update counter
        n += 1
